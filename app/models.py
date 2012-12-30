from django.db import models

class Show(models.Model):
    tvdbid = models.IntegerField(unique=True)
    name = models.TextField()
    status = models.TextField()
    banner = models.TextField()
    first_aired = models.DateTimeField(null=True)
    imdb = models.TextField()

    def get_seasons(self):
        return self.seasons.all().order_by('-number')

class Season(models.Model):
    number = models.IntegerField()
    show = models.ForeignKey(Show, related_name='seasons')

    def get_episodes(self):
        return self.episodes.all().order_by('-number')

class Episode(models.Model):
    number = models.IntegerField()
    season = models.ForeignKey(Season, related_name='episodes')
