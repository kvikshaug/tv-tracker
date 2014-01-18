from django.db import models
from django.db.models import Q

from datetime import datetime

class Show(models.Model):
    tvdbid = models.IntegerField(unique=True)
    name = models.TextField()
    status = models.TextField()
    banner = models.TextField()
    first_aired = models.DateTimeField(null=True)
    imdb = models.TextField()

    last_seen = models.CharField(max_length=255)
    comments = models.TextField()
    LOCAL_STATUS_CHOICES = (
        ('active', ''),
        ('default', ''),
        ('archived', ''),
    )
    local_status = models.CharField(max_length=255, choices=LOCAL_STATUS_CHOICES)

    def get_seasons(self):
        return self.seasons.all().order_by('-number')

    def get_seen_season(self):
        if self.last_seen == '':
            return 0
        else:
            return int(self.last_seen.split('x')[0])

    def get_seen_episode(self):
        if self.last_seen == '':
            return 0
        else:
            return int(self.last_seen.split('x')[1])

    def get_available_unseen(self):
        try:
            seen_season, seen_episode = self.last_seen.split('x')
        except ValueError:
            seen_season = 0
            seen_episode = 0

        now = datetime.now()
        available_episodes = Episode.objects.filter(
            Q(
                # Future episodes this season
                season__number=seen_season,
                number__gt=seen_episode
            ) | Q(
                # Future seasons
                season__number__gt=seen_season,
            ),
            season__show=self,
            air_date__lte=now,
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
        season = self.seasons.all().order_by('-number')[0]
        return season.episodes.all().order_by('-number')[0]

    def get_next_episode(self):
        future_episodes = Episode.objects.filter(season__show=self, air_date__gte=datetime.now()).order_by('air_date')
        if future_episodes.exists():
            return future_episodes[0]
        else:
            return None

class Season(models.Model):
    number = models.IntegerField()
    show = models.ForeignKey(Show, related_name='seasons')

    def get_episodes(self):
        return self.episodes.all().order_by('-number')

class Episode(models.Model):
    number = models.IntegerField()
    air_date = models.DateTimeField(null=True)
    season = models.ForeignKey(Season, related_name='episodes')

    def get_number(self):
        if self.number < 10:
            lazy_zero = '0'
        else:
            lazy_zero = ''
        return "%sx%s%s" % (self.season.number, lazy_zero, self.number)

    def get_days_remaining(self):
        return (self.air_date - datetime.now()).days + 1

    def get_status(self):
        seen_season = self.season.show.get_seen_season()
        seen_episode = self.season.show.get_seen_episode()

        if self.air_date > datetime.now():
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
