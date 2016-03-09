from itertools import groupby

from datetime import date

from django.db import models

class LastUpdate(models.Model):
    """Should only contain a single row."""
    datetime = models.DateTimeField()

    def __str__(self):
        return "%s: %s" % (self.pk, self.datetime)

class Series(models.Model):
    tvdbid = models.PositiveIntegerField(unique=True)
    name = models.TextField()
    status = models.TextField()
    banner = models.TextField()
    poster = models.CharField(max_length=255)
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

    def __str__(self):
        return "%s: %s" % (self.pk, self.name)

    def get_last_seen(self):
        if self.last_seen == '':
            return (0, 0)
        else:
            season, episode = self.last_seen.split('x')
            return (int(season), int(episode))

    def episodes_by_season(self):
        return [
            {'season': season, 'episodes': list(episodes)}
            for season, episodes in groupby(self.episodes.all(), key=lambda e: e.season)
        ]

    def episodes_by_season_reversed(self):
        """Reverse both season and episodes"""
        return [
            {'season': group['season'], 'episodes': reversed(group['episodes'])}
            for group in reversed(self.episodes_by_season())
        ]

    def unseen_episode_count(self):
        """Return the number of unseen episodes. Depends on having seasons and episodes prefetched for performance."""
        seen_season, seen_episode = self.get_last_seen()
        aired_episodes = [e for e in self.episodes.all() if e.air_date is not None and e.air_date <= date.today()]
        current_season = [e for e in aired_episodes if e.season == seen_season and e.episode > seen_episode]
        future_seasons = [e for e in aired_episodes if e.season > seen_season]
        return len(current_season) + len(future_seasons)

    def has_latest_available_episode(self):
        try:
            self.get_latest_available_episode()
            return True
        except IndexError:
            return False

    def get_latest_available_episode(self):
        aired_episodes = [e for e in self.episodes.all() if e.air_date is not None and e.air_date <= date.today()]
        return aired_episodes[-1]

    def has_next_episode_on_air(self):
        try:
            self.next_episode_on_air()
            return True
        except IndexError:
            return False

    def next_episode_on_air(self):
        unaired_episodes = [e for e in self.episodes.all() if e.air_date is not None and e.air_date > date.today()]
        return unaired_episodes[0]

    def last_episode(self):
        return list(self.episodes.all())[-1]

    def increase_seen(self):
        season, episode = self.get_last_seen()
        if season == 0:
            next = '1x01'
        else:
            if self.episodes.filter(season=season, episode=(episode + 1)).exists():
                # Next episode
                next = '%sx%02d' % (season, (episode + 1))
            elif self.episodes.filter(season=(season + 1), episode=1).exists():
                # Next season
                next = '%sx01' % (season + 1)
            else:
                # Seen it all
                return

        self.last_seen = next
        self.save()

    class Meta:
        ordering = ['name']

class Episode(models.Model):
    series = models.ForeignKey(Series, related_name='episodes')
    season = models.PositiveIntegerField()
    episode = models.PositiveIntegerField()
    air_date = models.DateField(null=True)

    def __str__(self):
        return "%s: %s (%s)" % (self.pk, self.episode_number(), self.series.name)

    def episode_number(self):
        return "%sx%02d" % (self.season, self.episode)

    def days_remaining(self):
        return (self.air_date - date.today()).days + 1

    def status_class(self):
        seen_season, seen_episode = self.series.get_last_seen()

        if self.air_date is None or self.air_date > date.today():
            return 'unaired'
        else:
            if self.season > seen_season:
                return 'available'
            elif self.season == seen_season:
                if self.episode > seen_episode:
                    return 'available'
                else:
                    return 'seen'
            else:
                return 'seen'

    class Meta:
        ordering = ['season', 'episode']
        unique_together = ('series', 'season', 'episode')
