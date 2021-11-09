from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from spotify.utils import checkSpotifyAuthentication
import random

# Api that gets pairs of songs and accepts results of swipes
class find(APIView):
	parser_classes = [JSONParser]
	def get(self, request, format=None):
		newTokens = self.authCheck(request.data)
		if(newTokens == None):
			access_token = request.data.get('access_token')
			refresh_token = request.data.get('refresh_token')
			expires_in = request.data.get('expires_in')
		else:
			access_token = newTokens.get('access_token')
			refresh_token = request.data.get('refresh_token')
			expires_in = newTokens.get('expires_in')

		return Response({'message': 'find works!'}, status=status.HTTP_200_OK)

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