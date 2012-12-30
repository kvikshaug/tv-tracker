from django.db import models

class Show(models.Model):
    tvdbid = models.IntegerField(unique=True)
    name = models.TextField()
    status = models.TextField()
    banner = models.TextField()
    first_aired = models.DateTimeField(null=True)
    imdb = models.TextField()

    last_seen = models.CharField(max_length=255)
    comments = models.TextField()

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

class Season(models.Model):
    number = models.IntegerField()
    show = models.ForeignKey(Show, related_name='seasons')

    def get_episodes(self):
        return self.episodes.all().order_by('-number')

class Episode(models.Model):
    number = models.IntegerField()
    season = models.ForeignKey(Season, related_name='episodes')
