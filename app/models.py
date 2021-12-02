from django.db import models

# TODO: Add entry for free/premium account
class User(models.Model):
	# session_id
	# user = models.CharField(max_length=60, unique=True, null=True)

	# User's Spotify display name
	display_name = models.CharField(max_length=150, null=True)
	# Email associated witn the users spotify account
	email = models.EmailField(max_length=150, unique=True, null=True)
	# Spotify ID
	spotify_id = models.CharField(max_length=150, unique=True, null=True)
	# Spotify API HREF
	spotify_href = models.CharField(max_length=200, unique=True, null=True)
	# SPOTIFY URI
	spotify_uri = models.CharField(max_length=150, unique=True, null=True)
	# Time user entry was created 
	created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
	# No of visits
	no_of_visits = models.PositiveIntegerField(null=True)

	def __str__(self):
		return (f"{self.spotify_id} (id:{self.id})")

class Song(models.Model):
	song_id = models.CharField(max_length=200, unique=True, blank=False)
	song_name = models.CharField(max_length=250, unique=True, null=True)
	points = models.FloatField(null=True)
	created_at = models.DateTimeField(auto_now_add=True, auto_now=False)