from django.contrib import admin
from .models import User

@admin.register(User)
class User(admin.ModelAdmin):
	list_display = ('display_name', 'spotify_id', 'email', 'user',
		'spotify_uri', 'created_at')
	fields =['user', 'display_name', 'email', 'spotify_id',
		'spotify_href', 'spotify_uri', 'created_at']