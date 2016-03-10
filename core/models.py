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

    def has_last_seen(self):
        return self.last_seen != ''

    def get_last_seen(self):
        if not self.has_last_seen():
            raise Exception("Last seen is undefined")

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
            {'season': group['season'], 'episodes': list(reversed(group['episodes']))}
            for group in reversed(self.episodes_by_season())
        ]

    def unseen_available(self):
        """Returns a dict of unseen aired episodes; the first and last in the range (or None if 0) and the count"""
        aired_episodes = [e for e in self.episodes.all() if e.air_date is not None and e.air_date <= date.today()]
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

    def unaired_episodes(self):
        return [e for e in self.episodes.all() if e.air_date is not None and e.air_date > date.today()]

    def has_next_episode_on_air(self):
        return len(self.unaired_episodes()) > 0

    def next_episode_on_air(self):
        return self.unaired_episodes()[0]

    def last_episode(self):
        return list(self.episodes.all())[-1]

    def increase_seen(self):
        # If we haven't seen anything, start on 1x01
        if not self.has_last_seen():
            self.last_seen = '1x01'
            self.save()
            return

        try:
            season, episode = self.get_last_seen()
            next_episode = self.episode_after(season, episode)
            self.last_seen = next_episode.episode_number()
            self.save()
        except Episode.DoesNotExist:
            # Seen it all; do nothing
            pass

    def episode_after(self, season, episode_number):
        for episode in self.episodes.all():
            if episode.season == season and episode.episode == episode_number + 1:
                return episode
            elif episode.season == season+1 and episode.episode == 1:
                return episode
        raise Episode.DoesNotExist("Series '%s' has no episode after %sx%02d" % (self, season, episode_number))

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
        if self.air_date is None or self.air_date > date.today():
            return 'unaired'
        else:
            if not self.series.has_last_seen():
                return 'available'

            seen_season, seen_episode = self.series.get_last_seen()
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
