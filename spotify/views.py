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
from app.models import User
from .utils import *

BASE_URL = "https://api.spotify.com/v1/"

# Request Authorization to access data
class AuthSpotify(APIView):
	def get(self, request, format=None):
		scopes = 'user-read-email' 
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
		expires_in = str(timezone.now() + timedelta(seconds=response.get('expires_in')))
		refresh_token = response.get('refresh_token')

		# Create a session if one does not exist
		if not request.session.exists(request.session.session_key):
			request.session.create()

		# Connect User Model here
		userData = get('http://192.168.1.101:8000/spotify/api/user/',
			json={
				'access_token': access_token,
				'refresh_token': refresh_token,
				'expires_in': expires_in
			}, 
			headers={
				'Content-type': 'application/json'
			})
		if(userData.ok):
			userData = userData.json()
			userProfile = User.objects.filter(spotify_id=userData.get('spotify_id'))
			if userProfile:
				userProfile = userProfile[0]
				userProfile.display_name = userData.get('display_name')
				userProfile.email = userData.get('email')
				userProfile.spotify_href = userData.get('spotify_href')
				userProfile.spotify_uri = userData.get('spotify_uri')
				userProfile.no_of_visits = userProfile.no_of_visits + 1
				userProfile.save(update_fields=['display_name', 'email',
					'spotify_href', 'spotify_uri', 'no_of_visits'])
			else:
				userProfile = User(
					display_name = userData.get('display_name'),
					email = userData.get('email'),
					spotify_id = userData.get('spotify_id'),
					spotify_href = userData.get('spotify_href'),
					spotify_uri = userData.get('spotify_uri'),
					no_of_visits = 1
					)
				userProfile.save()
			user_cover_image = userData.get('image')
		else:
			return redirect('main-app:app-welcome')

		# Create cookies with token data:
		response = redirect('main-app:app-home')
		cookie_max_age = 365*24*60*60
		# Set Cookies
		response.set_cookie('access_token', access_token, cookie_max_age, samesite='Lax')
		response.set_cookie('expires_in', expires_in, cookie_max_age, samesite='Lax')
		response.set_cookie('refresh_token', refresh_token, cookie_max_age, samesite='Lax')
		response.set_cookie('spotify_id', userData.get('spotify_id'), cookie_max_age, samesite='Lax')
		response.set_cookie('user_cover_image', user_cover_image, cookie_max_age, samesite='Lax')

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

# 
# Views that request specific information from executeSpotifyAPIRequest:
# 

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

		# Check if Spotify is authenticated
		newTokens = checkSpotifyAuthentication(tokens)
		if(newTokens == None):
			pass
		else:
			access_token = newTokens.get('access_token')
			expires_in = newTokens.get('expires_in')

		# Send get request to execute api
		tokens = {
			'access_token': access_token,
			'endpoint': 'me'
		}
		headers = {'Content-type': 'application/json'}
		try:
			spotifyResponse = get('http://192.168.1.101:8000/spotify/api/execute/',
				json=tokens, headers=headers)
		except:
			return Response({'error: Call to executeSpotifyAPIRequest Failed'}, status=status.HTTP_400_BAD_REQUEST)

		# Process spotifyResponse
		if(spotifyResponse.ok):
			# Clean JSON Response
			spotifyResponse = spotifyResponse.json()
			response = {
				'access_token': access_token,
				'expires_in': expires_in,
				'display_name': spotifyResponse.get('display_name'),
				'email': spotifyResponse.get('email'),
				'followers': spotifyResponse.get('followers').get('total'),
				'spotify_href': spotifyResponse.get('href'),
				'spotify_id': spotifyResponse.get('id'),
				'image': spotifyResponse.get('images')[0].get('url'),
				'spotify_uri': spotifyResponse.get('uri')
			}
			return Response(response, status=status.HTTP_200_OK)
		else:
			return Response(spotifyResponse.json(), status=status.HTTP_400_BAD_REQUEST)

# 
# Template Rendering Views:
# 

# Render Welcome Page (index.html)
def welcome(request):
	if not request.session.exists(request.session.session_key):
		request.session.create()
	return render(request, 'spotify/index.html')

# Render Home Page (home.html0
def home(request):
	return render(request, 'spotify/home.html')