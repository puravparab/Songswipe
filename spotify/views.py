# SPOTIFY API DOCUMENTAION:
# https://developer.spotify.com/documentation/general/guides/authorization/code-flow/

from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, parser_classes
from requests import Request, get, post, put
from .models import User
from .utils import *

BASE_URL = "https://api.spotify.com/v1/"

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

		# Response with token data
		access_token = response.get('access_token')
		token_type = response.get('token_type')
		expires_in = response.get('expires_in')
		refresh_token = response.get('refresh_token')

		# Create cookies with token data:
		response = redirect('spotify-home')
		expires_in = timezone.now() + timedelta(seconds=expires_in)
		cookie_max_age = 365*24*60*60

		# Set Cookies
		response.set_cookie('access_token', access_token, cookie_max_age, samesite='Lax')
		# response.set_cookie('token_type', token_type, cookie_max_age)
		response.set_cookie('expires_in', expires_in, cookie_max_age, samesite='Lax')
		response.set_cookie('refresh_token', refresh_token, cookie_max_age, samesite='Lax')

		# Create a session if one does not exist
		if not request.session.exists(request.session.session_key):
			request.session.create()

		# Connect User Model here

		return response

	elif error != None:
		context = {
			'error': error
		}
		return render(request, 'spotify/error.html', context)

# Execute an API request to the SPOTIFY API:
class executeSpotifyAPIRequest(APIView):
	parser_classes = [JSONParser]

	def get(self, request, format=None):
		access_token = request.data.get('access_token')
		endpoint = request.data.get('endpoint')

		# Creating headers
		headers = {'Content-type': 'application/json',
					'Authorization': 'Bearer ' + access_token}

		# request the Spotify API at the endpoint
		response = get(BASE_URL + endpoint, {}, headers=headers)

		if(response.ok == True):
			return Response(response.json(), status=status.HTTP_200_OK)
		else:
			return Response(response.json(), status=status.HTTP_400_BAD_REQUEST)

# Views that request specific information from executeSpotifyAPIRequest view:

# Request User Profile
@api_view(["GET"])
@parser_classes([JSONParser])
def currentUserProfile(request, format=None):
	if request.method == 'GET':
		access_token = request.data.get('access_token')
		refresh_token = request.data.get('refresh_token')
		expires_in = request.data.get('expires_in')
		# Create tokens to pass into isSpotifyAuthenicated function
		tokens = {
			'access_token': access_token,
			'refresh_token': refresh_token,
			'expires_in': expires_in
		}
		if isSpotifyAuthenticated(tokens):
			tokens = {
				'access_token': access_token,
				'endpoint': 'me'
			}
			headers = {'Content-type': 'application/json'}
			# Send get request to execute api
			response = get('http://192.168.1.101:8000/spotify/api/execute/',
				 json=tokens, headers=headers)
			if(response.ok == True):
				return Response(response.json(), status=status.HTTP_200_OK)
			else:
				return Response(response.json(), status=status.HTTP_400_BAD_REQUEST)
		else:
			# TODO: Auth = False
			return
			
# Template Rendering Views:

# Render Welcome Page (index.html)
def welcome(request):
	if not request.session.exists(request.session.session_key):
		request.session.create()
	return render(request, 'spotify/index.html')

# Render Home Page (home.html0
def home(request):
	return render(request, 'spotify/home.html')