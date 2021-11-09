from django.shortcuts import render
from requests import get
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from spotify.utils import checkSpotifyAuthentication
import random

# Api that gets pairs of songs and accepts results of swipes
class find(APIView):
	def get(self, request, format=None):
		access_token = request.COOKIES.get('access_token')
		refresh_token = request.COOKIES.get('refresh_token')
		expires_in = request.COOKIES.get('expires_in')
		tokens = {
			'access_token': access_token,
			'refresh_token': refresh_token,
			'expires_in': str(expires_in)
		}
		newTokens = self.authCheck(tokens)
		if(newTokens == None):
			pass
		else:
			access_token = newTokens.get('access_token')
			expires_in = newTokens.get('expires_in')

		# GET SONG PAIRS

		# return top 50 songs from users saved tracks and choose 25 songs at random
		limit = 50
		offset = 0
		tokens = {
			'access_token': access_token,
			'refresh_token': refresh_token,
			'expires_in': expires_in,
		}
		# TODO: ADD CASE IF USER DOES NOT HAVE SONGS
		try:
			ROOT_URL = request.build_absolute_uri('/')
			headers = {'Content-type': 'application/json'}
			response = get((f'{ROOT_URL}spotify/api/user/saved-tracks/{limit}/{offset}/'),
				json=tokens, headers=headers)
		except:
			return Response({'Error': 'Call to saved tracks API Failed'}, status=status.HTTP_400_BAD_REQUEST)

		return Response(response.json(), status=status.HTTP_200_OK)

	# Validate tokens
	def authCheck(self, tokens):
		access_token = tokens.get('access_token')
		refresh_token = tokens.get('refresh_token')
		expires_in = tokens.get('expires_in')
		# Create tokens to pass into checkSpotifyAuthenticated function
		tokens = {
			'access_token': access_token,
			'refresh_token': refresh_token,
			'expires_in': expires_in
		}
		# Check if Spotify is authenticated
		newTokens = checkSpotifyAuthentication(tokens)
		return newTokens