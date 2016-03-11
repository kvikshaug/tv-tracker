from datetime import date
from itertools import groupby

from django.contrib.auth.models import User
from django.db import models

class LastUpdate(models.Model):
    """Should only contain a single row."""
    datetime = models.DateTimeField()

    def __str__(self):
        return "%s: %s" % (self.pk, self.datetime)

class Watching(models.Model):
    user = models.ForeignKey(User, related_name='watches')
    series = models.ForeignKey('Series', related_name='users')
    last_seen = models.CharField(max_length=255)
    STATUS_CHOICES = [
        ('active', ''),
        ('default', ''),
        ('archived', ''),
    ]
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='default')

    def __str__(self):
        return "%s: %s watching %s" % (self.pk, self.user.username, self.series.name)

    def has_last_seen(self):
        return self.last_seen != ''

    def get_last_seen(self):
        if not self.has_last_seen():
            raise Exception("Last seen is undefined")

        season, episode = self.last_seen.split('x')
        return (int(season), int(episode))

    def unseen_available(self):
        """Returns a dict of unseen aired episodes; the first and last in the range (or None if 0) and the count"""
        aired_episodes = [
            e for e in self.series.episodes.all()
            if e.air_date is not None and
            e.air_date <= date.today()
        ]
        if not self.has_last_seen():
            # If we haven't seen anything, all aired episodes are unseen, according to tautology club
            unseen_available = aired_episodes
        else:
            seen_season, seen_episode = self.get_last_seen()
            unseen_available = [
                e for e in aired_episodes
                if (e.season == seen_season and e.episode > seen_episode) or
                e.season > seen_season
            ]

        if len(unseen_available) == 0:
            first = None
            last = None
        else:
            first = unseen_available[0]
            last = unseen_available[-1]

        return {
            'first': first,
            'last': last,
            'count': len(unseen_available),
        }

    def move_seen(self, direction='next'):
        if not self.has_last_seen():
            if direction == 'next':
                # If we're starting to watch, start with the pilot
                self.last_seen = '1x01'
                self.save()
                return
            else:
                # Decreasing without having seen anything anyway? Ignore
                return

        try:
            season, episode = self.get_last_seen()
            if direction == 'next':
                new_episode = self.series.episode_after(season, episode)
            else:
                # Special case: Trying to unset seen (decreasing when having only seen the pilot)
                if season == 1 and episode == 1:
                    self.last_seen = ''
                    self.save()
                    return

                new_episode = self.series.episode_before(season, episode)
            self.last_seen = new_episode.episode_number()
            self.save()
        except Episode.DoesNotExist:
            # Reached start/end or the last_seen value is invalid; do nothing
            pass

    class Meta:
        ordering = ['series__name']

class Series(models.Model):
    tvdbid = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=255)
    banner = models.CharField(max_length=255)
    poster = models.CharField(max_length=255)
    first_aired = models.DateField(null=True)
    imdb = models.CharField(max_length=1023)

    def __str__(self):
        return "%s: %s" % (self.pk, self.name)

    def episodes_by_season(self):
        return [
            {'season': season, 'episodes': list(episodes)}
            for season, episodes in groupby(self.episodes.all(), key=lambda e: e.season)
        ]

    def episodes_by_season_reversed(self):
        """Reverse both season and episodes"""
        return [
            {'season': group['season'], 'episodes': list(reversed(group['episodes']))}
            for group in reversed(self.episodes_by_season())
        ]

    def unaired_episodes(self):
        return [e for e in self.episodes.all() if e.air_date is not None and e.air_date > date.today()]

    def has_next_episode_on_air(self):
        return len(self.unaired_episodes()) > 0

    def next_episode_on_air(self):
        return self.unaired_episodes()[0]

    def last_episode(self):
        return list(self.episodes.all())[-1]

    def episode_before(self, season, episode_number):
        if episode_number == 1:
            previous_season = [e for e in self.episodes.all() if e.season == season - 1]
            if len(previous_season) == 0:
                raise Episode.DoesNotExist("Series '%s' has no season before %sx%02d" % (self, season, episode_number))
            return max(previous_season, key=lambda e: e.episode)
        else:
            for episode in self.episodes.all():
                if episode.season == season and episode.episode == episode_number - 1:
                    return episode
            raise Episode.DoesNotExist("Series '%s' has no episode before %sx%02d" % (self, season, episode_number))

    def episode_after(self, season, episode_number):
        for episode in self.episodes.all():
            if episode.season == season and episode.episode == episode_number + 1:
                return episode
            elif episode.season == season + 1 and episode.episode == 1:
                return episode
        raise Episode.DoesNotExist("Series '%s' has no episode after %sx%02d" % (self, season, episode_number))

    @staticmethod
    def create_or_sync(tvdbid):
        try:
            return Series.objects.get(tvdbid=tvdbid)
        except Series.DoesNotExist:
            from thetvdb import tvdb
            return tvdb.create_or_update_series(tvdbid)

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

    class Meta:
        ordering = ['season', 'episode']
        unique_together = ('series', 'season', 'episode')
