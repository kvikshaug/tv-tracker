from django.db import models

class Series(models.Model):
    name = models.TextField()

class Season(models.Model):
    number = models.IntegerField()
    series = models.ForeignKey(Series)

class Episode(models.Model):
    number = models.IntegerField()
    season = models.ForeignKey(Season)
