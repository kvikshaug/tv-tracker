from datetime import date

from django.db import models

class LastUpdate(models.Model):
    """Should only contain a single row."""
    datetime = models.DateTimeField()

class Series(models.Model):
    tvdbid = models.PositiveIntegerField(unique=True)
    name = models.TextField()
    status = models.TextField()
    banner = models.TextField()
    first_aired = models.DateField(null=True)
    imdb = models.TextField()

    last_seen = models.CharField(max_length=255)
    comments = models.TextField()
    LOCAL_STATUS_CHOICES = [
        ('active', ''),
        ('default', ''),
        ('archived', ''),
    ]
    local_status = models.CharField(max_length=255, choices=LOCAL_STATUS_CHOICES, default='default')

    def get_last_seen(self):
        if self.last_seen == '':
            return (0, 0)
        else:
            season, episode = self.last_seen.split('x')
            return (int(season), int(episode))

    def unseen_episode_count(self):
        """Return the number of unseen episodes. Depends on having seasons and episodes prefetched for performance."""
        seen_season, seen_episode = self.get_last_seen()
        count = 0
        for season in self.seasons.all():
            if season.number == seen_season:
                # Current season
                count += len([
                    e for e in season.episodes.all()
                    if e.air_date is not None and
                    e.air_date <= date.today() and
                    e.number > seen_episode
                ])
            elif season.number > seen_season:
                # Future season
                count += len([
                    e for e in season.episodes.all()
                    if e.air_date is not None and
                    e.air_date <= date.today()
                ])
        return count

    def get_all_episodes(self):
        return [e for s in self.seasons.all() for e in s.episodes.all()]

    def get_aired_episodes(self):
        return [e for e in self.get_all_episodes() if e.air_date is not None and e.air_date <= date.today()]

    def has_latest_available_episode(self):
        try:
            self.get_latest_available_episode()
            return True
        except IndexError:
            return False

    def get_latest_available_episode(self):
        aired_episodes = self.get_aired_episodes()
        return aired_episodes[0]

    def get_future_episodes(self):
        return [e for e in self.get_all_episodes() if e.air_date is not None and e.air_date > date.today()]

    def has_next_episode(self):
        try:
            self.get_next_episode()
            return True
        except IndexError:
            return False

    def get_next_episode(self):
        future_episodes = sorted(self.get_future_episodes(), key=lambda e: e.air_date)
        return future_episodes[0]

    def get_newest_episode(self):
        return self.get_all_episodes()[0]

    def increase_seen(self):
        season, episode = self.get_last_seen()
        if season == 0:
            next = '1x01'
        else:
            if self.seasons.filter(number=season, episodes__number=(episode + 1)).exists():
                # Next episode
                next = '%sx%02d' % (season, (episode + 1))
            elif self.seasons.filter(number=(season + 1), episodes__number=1).exists():
                # Next season
                next = '%sx01' % (season + 1)
            else:
                # Seen it all
                return

        self.last_seen = next
        self.save()

    class Meta:
        ordering = ['name']

class Season(models.Model):
    number = models.PositiveIntegerField()
    series = models.ForeignKey(Series, related_name='seasons')

    class Meta:
        ordering = ['-number']

class Episode(models.Model):
    number = models.PositiveIntegerField()
    air_date = models.DateField(null=True)
    season = models.ForeignKey(Season, related_name='episodes')

    def get_number(self):
        return "%sx%02d" % (self.season.number, self.number)

    def get_days_remaining(self):
        return (self.air_date - date.today()).days + 1

    def get_status_class(self):
        seen_season, seen_episode = self.season.series.get_last_seen()

        if self.air_date is None or self.air_date > date.today():
            return 'unaired'
        else:
            if self.season.number > seen_season:
                return 'available'
            elif self.season.number == seen_season:
                if self.number > seen_episode:
                    return 'available'
                else:
                    return 'seen'
            else:
                return 'seen'

    class Meta:
        ordering = ['-number']
