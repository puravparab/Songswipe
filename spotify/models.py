from django.db import models

class User(models.Model):
	# session_id
	user = models.CharField(max_length=60, unique=True, null=True)
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
	visits = models.PositiveIntegerField(null=True)