from django.db import models
from django.db.models import Q

from datetime import date

class LastUpdate(models.Model):
    """Should only contain a single row."""
    date = models.DateTimeField()

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

    def get_available_unseen(self):
        seen_season, seen_episode = self.get_last_seen()
        available_episodes = Episode.objects.filter(
            Q(
                # Future episodes this season
                season__number=seen_season,
                number__gt=seen_episode
            ) | Q(
                # Future seasons
                season__number__gt=seen_season,
            ),
            season__series=self,
            air_date__lte=date.today(),
        )
        latest = None
        for e in available_episodes:
            if latest is None:
                latest = e
                continue

            if e.season.number > latest.season.number:
                latest = e
                continue

            if e.season.number == latest.season.number and e.number > latest.number:
                latest = e
                continue
        return {
            'latest': latest,
            'count': len(available_episodes)
        }

    def get_newest_episode(self):
        return self.seasons.all()[0].episodes.all()[0]

    def get_next_episode(self):
        future_episodes = Episode.objects.filter(season__series=self, air_date__gt=date.today()).order_by('air_date')
        if future_episodes.exists():
            return future_episodes[0]
        else:
            return None

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
