from django.db import models
from user.models import CustomUser


class Genre(models.Model):
    name = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class AvailablePlatformsMovie(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class StreamPlatform(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    available_movie = models.ManyToManyField(AvailablePlatformsMovie)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=250)
    genre = models.ManyToManyField(Genre)
    synopsis = models.TextField()
    runtime = models.IntegerField()
    stream_platform = models.ManyToManyField(StreamPlatform)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class WatchList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.movie


class MovieReview(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    review = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.movie
