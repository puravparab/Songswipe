from django.contrib import admin
from .models import User, Song

@admin.register(User)
class User(admin.ModelAdmin):
	list_display = ('spotify_id', 'display_name', 'email',
		'spotify_uri', 'created_at', 'no_of_visits')
	fields =['display_name', 'email', 'spotify_id',
		'spotify_href', 'spotify_uri', 'no_of_visits']

@admin.register(Song)
class Song(admin.ModelAdmin):
	list_display = ('song_name', 'song_id', 'points', 'created_at')
	fields =['song_name', 'song_id', 'points']