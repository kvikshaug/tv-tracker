from django.db import models

class Show(models.Model):
    tvdbid = models.IntegerField(unique=True)
    name = models.TextField()

class Season(models.Model):
    number = models.IntegerField()
    show = models.ForeignKey(Show)

class Episode(models.Model):
    number = models.IntegerField()
    season = models.ForeignKey(Season)
