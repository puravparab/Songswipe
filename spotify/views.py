# SPOTIFY API DOCUMENTAION:
# https://developer.spotify.com/documentation/general/guides/authorization/code-flow/

from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from requests import Request, get, post, put
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, parser_classes
from app.models import User
from .utils import *

# Request Authorization to access data
class AuthSpotify(APIView):
	def get(self, request, format=None):
		scopes = 'user-read-email user-read-private user-library-read user-library-modify' 
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

	print(f'code:{code}')
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

		print(f'response:{response}')
		# Response with token data
		access_token = response.get('access_token')
		token_type = response.get('token_type')
		expires_in = str(timezone.now() + timedelta(seconds=response.get('expires_in')))
		refresh_token = response.get('refresh_token')

		# Create a session if one does not exist
		if not request.session.exists(request.session.session_key):
			request.session.create()

		# TODO: REDUCE API REQUESTS. ADD Auth check before API call

		# Connect User Model here
		ROOT_URL = request.build_absolute_uri('/')
		print(f'ROOT_URL:{ROOT_URL}')
		userData = get((f'{ROOT_URL}spotify/api/user/'),
			json={
				'access_token': access_token,
				'refresh_token': refresh_token,
				'expires_in': expires_in
			}, 
			headers={
				'Content-type': 'application/json'
			})
		print(f'user_data:{userData}')
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
			print('redirecting...')
			return redirect('main-app:app-welcome')

		# Create cookies with token data:
		response = redirect('main-app:app-home')
		cookie_max_age = 365*24*60*60
		# Set Cookies
		response.set_cookie('access_token', access_token, cookie_max_age, samesite='Lax')
		response.set_cookie('expires_in', expires_in, cookie_max_age, samesite='Lax')
		response.set_cookie('refresh_token', refresh_token, cookie_max_age, samesite='Lax')
		response.set_cookie('spotify_id', userData.get('spotify_id'), cookie_max_age, samesite='Lax')
		response.set_cookie('display_name', userData.get('display_name'), cookie_max_age, samesite='Lax')
		response.set_cookie('user_cover_image', user_cover_image, cookie_max_age, samesite='Lax')

		print(f'response_callback:{response}')
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
		BASE_URL = "https://api.spotify.com/v1/"
		# Creating headers
		headers = {'Content-type': 'application/json',
					'Authorization': 'Bearer ' + access_token}
		# Creating url parameters
		params = {
			'limit': request.data.get('limit'),
			'offset': request.data.get('offset'),
			'ids': request.data.get('ids')
		}
		# request the Spotify API at the endpoint
		try:
			response = get(BASE_URL + endpoint, headers=headers, params=params)
		except Exception as e:
			print(f'executeAPI:{str(e)}')
			return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

		if(response.ok):
			return Response(response.json(), status=status.HTTP_200_OK)
		else:
			print('execute fetching nothing')
			return Response(response, status=status.HTTP_400_BAD_REQUEST)

	def put(self, request, format=None):
		access_token = request.data.get('access_token')
		endpoint = request.data.get('endpoint')
		BASE_URL = "https://api.spotify.com/v1/"
		# Creating headers
		headers = {'Content-type': 'application/json',
					'Authorization': 'Bearer ' + access_token}
		# Creating url parameters
		params = {
			'limit': request.data.get('limit'),
			'offset': request.data.get('offset'),
			'ids': request.data.get('ids')
		}
		# request the Spotify API at the endpoint
		try:
			response = put(BASE_URL + endpoint, headers=headers, params=params)
		except Exception as e:
			print(f'executeAPI:{str(e)}')
			return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

		if(response.ok):
			return Response(response, status=status.HTTP_200_OK)
		else:
			print('execute fetching nothing')
			return Response(response, status=status.HTTP_400_BAD_REQUEST)

# 
# Views that request specific information from executeSpotifyAPIRequest:
#

# Request User Profile
# https://developer.spotify.com/documentation/web-api/reference/#/operations/get-current-users-profile
# TODO: REFACTOR TO CLASS BASED VIEW
@api_view(["GET"])
@parser_classes([JSONParser])
def currentUserProfile(request, format=None):
	if request.method == 'GET':
		access_token = request.data.get('access_token')
		refresh_token = request.data.get('refresh_token')
		expires_in = request.data.get('expires_in')

		# Create tokens to pass into checkSpotifyAuthenticated function
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
			ROOT_URL = request.build_absolute_uri('/')
			spotifyResponse = get((f'{ROOT_URL}spotify/api/execute/'),
				json=tokens, headers=headers)
		except:
			return Response({'Error: Call to executeSpotifyAPIRequest Failed'}, status=status.HTTP_400_BAD_REQUEST)

		# Process spotifyResponse
		if(spotifyResponse.ok):
			print(f'spotify_response:{spotifyResponse.json()}')
			# Clean JSON Response
			spotifyResponse = spotifyResponse.json()
			# If image does not exist
			try:
				image = spotifyResponse.get('images')[0].get('url')
			except:
				image = ""
			response = {
				'access_token': access_token,
				'expires_in': expires_in,
				'display_name': spotifyResponse.get('display_name'),
				'email': spotifyResponse.get('email'),
				'followers': spotifyResponse.get('followers').get('total'),
				'spotify_href': spotifyResponse.get('href'),
				'spotify_id': spotifyResponse.get('id'),
				'image': image,
				'spotify_uri': spotifyResponse.get('uri')
			}
			return Response(response, status=status.HTTP_200_OK)
		else:
			# return Response(spotifyResponse.json(), status=status.HTTP_400_BAD_REQUEST)
			print(f'spotify_response:{spotifyResponse}')
			return Response({'error': spotifyResponse}, status=status.HTTP_400_BAD_REQUEST)

# Get user's saved tracks
# https://developer.spotify.com/documentation/web-api/reference/#/operations/get-users-saved-tracks
class userSavedTracks(APIView):
	parser_classes = [JSONParser]
	def get(self, request, limit, offset):
		newTokens = self.authCheck(request.data)
		if(newTokens == None):
			access_token = request.data.get('access_token')
			refresh_token = request.data.get('refresh_token')
			expires_in = request.data.get('expires_in')
		else:
			access_token = newTokens.get('access_token')
			refresh_token = request.data.get('refresh_token')
			expires_in = newTokens.get('expires_in')

		# Send get request to execute api
		tokens = {
			'access_token': access_token,
			'endpoint': 'me/tracks',
			'limit': str(limit),
			'offset': str(offset)
		}
		headers = {'Content-type': 'application/json'}
		try:
			ROOT_URL = request.build_absolute_uri('/')
			spotifyResponse = get((f'{ROOT_URL}spotify/api/execute/'),
				json=tokens, headers=headers)
		except:
			return Response({'Error: Call to executeSpotifyAPIRequest Failed'}, status=status.HTTP_400_BAD_REQUEST)

		if(spotifyResponse.ok):
			response = self.cleanResponse(spotifyResponse.json())
			response['access_token'] = access_token
			response['expires_in'] = expires_in
			return Response(response, status=status.HTTP_200_OK)
		else:
			return Response(spotifyResponse.json(), status=status.HTTP_400_BAD_REQUEST)

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

	# Cleans data saved track data from spotify 
	def cleanResponse(self, jsonData):
		count = 0
		items = []
		for item in jsonData.get('items'):
			count = count + 1
			# Store track metadata
			track = {
				'name': item.get('track').get('name'),
				'id': item.get('track').get('id'),
				'duration_ms': item.get('track').get('duration_ms'),
				'popularity': item.get('track').get('popularity'),
				'uri': item.get('track').get('uri'),
				'url': item.get('track').get('external_urls').get('spotify'),
				'preview_url': item.get('track').get('preview_url'),
				'artists': [],
			}
			# Store artist(s) metadata
			for artists in item.get('track').get('artists'):
				artist = {
					'name': artists.get('name'),
					'id': artists.get('id'),
					'uri': artists.get('uri'),
					'url': artists.get('external_urls').get('spotify')
				}
				# add artist to track json
				track.get('artists').append(artist)
			# Store album metadata
			album = item.get('track').get('album')
			albumCleaned = {
				'name': album.get('name'),
				'id': album.get('id'),
				'uri': album.get('uri'),
				'url': album.get('external_urls').get('spotify'),
				'album_type': album.get('album_type'),
				'total_tracks': album.get('total_tracks'),
				# 640 x 640 cover image
				'image': album.get('images')[0].get('url')
			}
			# add album to track json
			track['album'] = albumCleaned
			# add cover image 
			track['cover_image'] = item.get('track').get('album').get('images')[0].get('url')
			# add the track in response json
			items.append(track)

		response = {
			'limit': jsonData.get('limit'),
			'total_saved': jsonData.get('total'),
			'total_items': count,
			'items': items
		}
		return response

# Check if track(s) is saved in user's library
# https://developer.spotify.com/documentation/web-api/reference/#/operations/check-users-saved-tracks
class verifyTracksSaved(APIView):
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

		# Parse through the list of song ids and check if they exist in the user's library
		# Spotify API accepts only 50 ids at a time
		id_list = request.data.get('ids').split(',')
		id_list_length = len(id_list)
		id_count = 0
		index = 0
		index_add = 0
		new_id_list = ""
		items = []
		headers = {'Content-type': 'application/json'}
		ROOT_URL = request.build_absolute_uri('/')
		tokens = {
			'access_token': access_token,
			'endpoint': 'me/tracks/contains'
		}
		while(True):
			# if loop has reached end of id_list
			if((index + index_add) >= id_list_length):
				new_id_list = new_id_list[:-1]
				# Send get request to execute api
				tokens["ids"] = new_id_list
				try:
					spotifyResponse = get((f'{ROOT_URL}spotify/api/execute/'), json=tokens, headers=headers)
				except:
					return Response({'Error: Call to executeSpotifyAPIRequest Failed'}, status=status.HTTP_400_BAD_REQUEST)
				if(spotifyResponse.ok):
					items += spotifyResponse.json()
				break
			elif(index <= 49):
				new_id_list += (f'{id_list[index + index_add]},')
				index += 1
			# if index is larger than 50
			else:
				new_id_list = new_id_list[:-1]
				# Send get request to execute api
				tokens["ids"] = new_id_list
				try:
					spotifyResponse = get((f'{ROOT_URL}spotify/api/execute/'), json=tokens, headers=headers)
				except:
					return Response({'Error: Call to executeSpotifyAPIRequest Failed'}, status=status.HTTP_400_BAD_REQUEST)
				if(spotifyResponse.ok):
					items += spotifyResponse.json()
				new_id_list = ""
				index = 0
				index_add = 50
		response = {
			"items": items
		}
		return Response(response, status=status.HTTP_200_OK)

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

# Add a track to the user's library:
# https://developer.spotify.com/documentation/web-api/reference/#/operations/save-tracks-user
class addTracksToLibrary(APIView):
	parser_classes = [JSONParser]
	def put(self, request, format=None):
		newTokens = self.authCheck(request.data)
		if(newTokens == None):
			access_token = request.data.get('access_token')
			refresh_token = request.data.get('refresh_token')
			expires_in = request.data.get('expires_in')
		else:
			access_token = newTokens.get('access_token')
			refresh_token = request.data.get('refresh_token')
			expires_in = newTokens.get('expires_in')

		headers = {'Content-type': 'application/json'}
		ROOT_URL = request.build_absolute_uri('/')
		tokens = {
			'access_token': access_token,
			'endpoint': 'me/tracks',
			'ids': request.data.get('ids')
		}
		try:
			spotifyResponse = put((f'{ROOT_URL}spotify/api/execute/'), json=tokens, headers=headers)
		except:
			return Response({'Error: Call to executeSpotifyAPIRequest Failed'}, status=status.HTTP_400_BAD_REQUEST)
		if spotifyResponse.ok:
			return Response(spotifyResponse.json(), status=status.HTTP_200_OK)
		else:
			return Response(spotifyResponse.json(), status=status.HTTP_400_BAD_REQUEST)

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
# 
# Template Rendering Views:
# 

# Render Welcome Page (index.html)
def welcome(request):
	if not request.session.exists(request.session.session_key):
		request.session.create()
	return render(request, 'spotify/index.html')

# Render Home Page (home.html)
def home(request):
	return render(request, 'spotify/home.html')