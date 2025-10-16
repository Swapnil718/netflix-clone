from django.conf import settings
from django.db import models

class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    overview = models.TextField(blank=True)
    poster_path = models.CharField(max_length=255, blank=True)
    backdrop_path = models.CharField(max_length=255, blank=True)
    trailer_youtube_key = models.CharField(max_length=50, blank=True)

    def poster_url(self):
        return f"https://image.tmdb.org/t/p/w500{self.poster_path}" if self.poster_path else ""

    def backdrop_url(self):
        return f"https://image.tmdb.org/t/p/original{self.backdrop_path}" if self.backdrop_path else ""

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    avatar = models.CharField(max_length=50, default="🙂")
    my_list = models.ManyToManyField(Movie, blank=True)

    def __str__(self):
        return f"{self.user.username}-{self.name}"
class Watch(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seconds = models.IntegerField(default=1)          # simple demo progress
    finished = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("profile", "movie")        # one row per profile+movie

    def __str__(self):
        return f"{self.profile} → {self.movie} ({'done' if self.finished else 'in progress'})"
