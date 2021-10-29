# SPOTIFY API DOCUMENTAION:
# https://developer.spotify.com/documentation/general/guides/authorization/code-flow/

from django.shortcuts import render, redirect
from django.conf import settings
from rest_framework.views import APIView
from requests import Request, post

# Request Authorization to access data
class AuthSpotify(APIView):
	def get(self, request, format=None):
		scopes = '' 
		url = Request('GET', 'https://accounts.spotify.com/authorize',
			params={
				'client_id': settings.SPOTIFY_CLIENT_ID,
				'response_type': 'code',
				'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
				'scope': scopes,
				# state
			}).prepare().url
		return redirect(url)

# Callback function:
# Spotify API redirects to this function (redirect_uri) after the user logs in
def callback(request, format=None):
	code = request.GET.get('code')
	error = request.GET.get('error')

	if code != None:
		# Request access tokens and refresh tokens
		response = post('https://accounts.spotify.com/api/token',
			data={
				'grant_type': 'authorization_code',
				'code': code,
				'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
				'client_id': settings.SPOTIFY_CLIENT_ID,
				'client_secret': settings.SPOTIFY_CLIENT_SECRET,
			}).json()

		# Response 
		access_token = response.get('access_token')
		token_type = response.get('token_type')
		expires_in = response.get('expires_in')
		refresh_token = response.get('refresh_token')

		return render(request, 'spotify/index.html')

	elif error != None:
		context = {
			'error': error
		}
		return render(request, 'spotify/error.html', context)
