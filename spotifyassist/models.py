from django.db import models
from django.contrib.auth.models import User


class Artist(models.Model):
    name = models.CharField(max_length=64)
    spotify_id = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class Track(models.Model):
    title = models.CharField(max_length=64)
    artist = models.ForeignKey(Artist,  on_delete=models.CASCADE, null=True)
    spotify_id = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.title} by {self.artist}"

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)        
    bannedTracks = models.ManyToManyField(Track, blank=True)

    def __str__(self):
        return self.user.username

class ArtistList(models.Model):
    list_name =  models.CharField(max_length=64)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artists = models.ManyToManyField(Artist, blank=True, related_name="artists") 

    def __str__(self):
        return self.list_name        

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    tracks = models.ManyToManyField(Track, blank=True) 
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=268) 

    def __str__(self):
        return f"{self.name} Playlist by {self.user}"