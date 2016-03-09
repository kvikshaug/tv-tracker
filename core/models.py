from itertools import groupby

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

    def get_aired_episodes(self):
        return [e for e in self.episodes.all() if e.air_date is not None and e.air_date <= date.today()]

    def has_latest_available_episode(self):
        try:
            self.get_latest_available_episode()
            return True
        except IndexError:
            return False

    def get_latest_available_episode(self):
        aired_episodes = self.get_aired_episodes()
        return list(aired_episodes)[-1]

    def get_future_episodes(self):
        return [e for e in self.episodes.all() if e.air_date is not None and e.air_date > date.today()]

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

    def get_number(self):
        return "%sx%02d" % (self.season, self.episode)

    def get_days_remaining(self):
        return (self.air_date - date.today()).days + 1

    def get_status_class(self):
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
