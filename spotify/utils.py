from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from requests import post

# Checks if spotify is authenticated. Creates new tokens if its not.
def checkSpotifyAuthentication(tokens):
	if isSpotifyAuthenticated(tokens):
		return None
	else:
		newTokens = refreshSpotifyToken(tokens.get('refresh_token'))
		# newTokens contains the new access_token and expires_in
		return newTokens

# Returns True if spotify is authenticated
def isSpotifyAuthenticated(tokens):
	access_token = tokens.get('access_token')
	refresh_token = tokens.get('refresh_token')
	expires_in = tokens.get('expires_in')
	expires_in = datetime.fromisoformat(expires_in)
	if (expires_in <= timezone.now()):
		return False
	else:
		return True

# Use refresh token to get a new access token
def refreshSpotifyToken(refresh_token):
	print('tokens refreshed')
	response = post('https://accounts.spotify.com/api/token',
		data={
			'grant_type': 'refresh_token',
			'refresh_token': refresh_token,
			'client_id': settings.SPOTIFY_CLIENT_ID,
			'client_secret': settings.SPOTIFY_CLIENT_SECRET
		}).json()
	tokens = {
		'access_token': response.get('access_token'),
		'expires_in': str(timezone.now() + timedelta(seconds=response.get('expires_in')))
	}
	return tokens
