# SPOTIFY API DOCUMENTAION:
# https://developer.spotify.com/documentation/general/guides/authorization/code-flow/

from django.shortcuts import render, redirect
from django.conf import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from rest_framework.views import APIView
from requests import Request

# Request Authorization to access data
class AuthSpotify(APIView):
	def get(self, request, format=None):
		scopes = '' 
		url = Request('GET', 'https://accounts.spotify.com/authorize',
			params={
				'client_id': SPOTIFY_CLIENT_ID,
				'response_type': 'code',
				'redirect_uri': ,
				'scope': scopes,
			}).prepare().url
		return redirect(url)

# Callback function:
# Spotify API redirects to this function (redirect_uri) after the user logs in
 