from django.db import models
from django.conf import settings
from guns.models import Gun


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField(null=True, blank=True)
    popularity = models.FloatField(null=True, blank=True)
    vote_count = models.IntegerField(null=True, blank=True)
    vote_average = models.FloatField(null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    poster_path = models.CharField(max_length=200, null=True, blank=True)
    original_title = models.CharField(max_length=100, null=True, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies', blank=True)
    related_guns = models.ManyToManyField(Gun, related_name='related_movies', blank=True)

    def __str__(self):
        return self.title

    # class Meta:
    #     ordering = ['title']