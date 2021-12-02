from django.shortcuts import render
from requests import get, post
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from spotify.utils import checkSpotifyAuthentication
from app.models import Song
import random

# Api that gets pairs of songs and accepts results of swipes
# TODO: make sure one pair doesnt have the same songs
class find(APIView):
	parser_classes = [JSONParser]

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

		# Return top 50 songs from users saved tracks and choose 25 songs at random
		limit = 50
		offset = 0
		tokens = {
			'access_token': access_token,
			'refresh_token': refresh_token,
			'expires_in': expires_in,
		}
		# TODO: ADD CASE IF USER DOES NOT HAVE ANY SONGS SAVED
		try:
			ROOT_URL = request.build_absolute_uri('/')
			headers = {'Content-type': 'application/json'}
			response = get((f'{ROOT_URL}spotify/api/user/saved-tracks/{limit}/{offset}/'),
				json=tokens, headers=headers)
		except:
			return Response({'Error': 'Call to saved tracks API Failed'}, 
				status=status.HTTP_400_BAD_REQUEST)

		total_song_count = 0
		songList = []
		if(response.ok):
			response = response.json()
			total_in_library = response.get('total_saved')
			total_items = response.get('total_items')
			count = 0
			while (True):
				if not count >= 25:
					index = random.randint(0,total_items-1)
					if(response.get('items')[index].get('preview_url') == None):
						pass
					else:
						songList.append(response.get('items')[index])
						count = count + 1
				else:
					break
			total_song_count = total_song_count + count
			# print(total_song_count)
			# update tokens if neccesary
			temp_access_token = response.get('access_token')
			temp_expires_in = response.get('expires_in')
			if(temp_expires_in != None and temp_expires_in != None):
				access_token = temp_access_token
				expires_in = temp_expires_in
		else:
			Response(response.json(), status=status.HTTP_400_BAD_REQUEST)

		# Return 50 songs at random from the library and choose 10. Continue until 
		# total_song_count equals 80
		while (total_song_count < 80):
			# TODO: ADD CASE IF USER HAS LESS THAN 50 SONGS
			limit = 50
			offset = random.randint(0, total_in_library-limit-1)
			tokens = {
				'access_token': access_token,
				'refresh_token': refresh_token,
				'expires_in': expires_in,
			}
			try:
				ROOT_URL = request.build_absolute_uri('/')
				headers = {'Content-type': 'application/json'}
				response = get((f'{ROOT_URL}spotify/api/user/saved-tracks/{limit}/{offset}/'),
					json=tokens, headers=headers)
			except:
				return Response({'Error': 'Call to saved tracks API Failed'}, 
					status=status.HTTP_400_BAD_REQUEST)

			if(response.ok):
				response = response.json()
				total_items = response.get('total_items')
				count = 0
				while (True):
					if count < 10 and total_song_count < 80:
						index = random.randint(0, total_items - 1)
						if(response.get('items')[index].get('preview_url') == None):
							pass
						else:
							songList.append(response.get('items')[index])
							count = count + 1
							total_song_count = total_song_count + 1
					else:
						break
				# print(total_song_count)

				# update tokens if neccesary
				temp_access_token = response.get('access_token')
				temp_expires_in = response.get('expires_in')
				if(temp_expires_in != None and temp_expires_in != None):
					access_token = temp_access_token
					expires_in = temp_expires_in
			else:
				Response(response.json(), status=status.HTTP_400_BAD_REQUEST)

		# Check if the each song is present in the user's library
		id_list = ""
		for song in songList:
			song_id = song.get("id")
			id_list += (f'{song_id},')
		tokens = {
			'access_token': access_token,
			'refresh_token': refresh_token,
			'expires_in': expires_in,
			'ids': id_list
		}
		try:
			ROOT_URL = request.build_absolute_uri('/')
			headers = {'Content-type': 'application/json'}
			response = get((f'{ROOT_URL}spotify/api/user/saved-tracks/check/'),
				json=tokens, headers=headers)
		except:
			return Response(response.json(), status=status.HTTP_400_BAD_REQUEST)
		if(response.ok):
			response = response.json()
			index = 0
			song_save_check = response.get("items")
			for song in songList:
				if(song_save_check[index] == True):
					song["in_library"] = True
				else:
					song["in_library"] = False
				index += 1

		# Use songList to make a list of randomly paired songs
		# stored in pair_list
		songListCopy = songList
		pair_list = []
		pair_count = 0
		while (True): 
			songs_pairs = []
			length = len(songList)
			if(pair_count < 40):
				# If only one song is left in songList
				if(length == 1):
					songs_pairs.append(songListCopy.pop(0))
					length = len(songList)
					pair_count = pair_count + 1
				else:
					# Song no 1
					index = random.randint(0, length - 1)
					songs_pairs.append(songListCopy.pop(index))
					length = len(songList)

					# Song no 2
					index = random.randint(0, length - 1)
					songs_pairs.append(songListCopy.pop(index))
					length = len(songList)

					pair_count = pair_count + 1
				pair_list.append(songs_pairs)
			else:
				break

		# Create songs
		songs = {
			'total_pairs': pair_count,
			'pair_list': pair_list
		}

		response = Response(songs, status=status.HTTP_200_OK)
		# Create cookies with token data:
		cookie_max_age = 365*24*60*60
		# Set Cookies
		response.set_cookie('access_token', access_token, cookie_max_age, samesite='Lax')
		response.set_cookie('expires_in', expires_in, cookie_max_age, samesite='Lax')
		return response

	def post(self, request, format=None):
		data = request.data.get("pair_data")
		results = request.data.get("results")
		print("asdas")
		print(results)

		Points = {}
		index = 0
		for pair in data.get("pair_list"):
			print(index)
			winner = results.get("winners")[index]
			if(winner == 0):
				loser = 1
			else:
				loser = 0

			id_A = data.get("pair_list")[index][0].get("id")
			popularity_A = data.get("pair_list")[index][0].get("popularity")
			id_B = data.get("pair_list")[index][1].get("id")
			popularity_B = data.get("pair_list")[index][1].get("popularity")
			id_list = [id_A, id_B]
			popularity = [popularity_A, popularity_B]

			points_diff_winner = 1 * (popularity[winner]/100)
			points_diff_loser = -1 * (popularity[loser]/100)

			if(Points.get(id_list[winner]) != None):
				Points[id_list[winner]]["points"] = Points.get(id_list[winner]).get("points") + points_diff_winner
			else:
				Points[id_list[winner]] = {
					'points': points_diff_winner,
					'display_name': data.get("pair_list")[index][winner].get("name")
				}

			if(Points.get(id_list[loser]) != None):
				Points[id_list[loser]]["points"] = Points.get(id_list[loser]).get("points") + points_diff_loser
			else:
				Points[id_list[loser]] = {
					'points': points_diff_loser,
					'display_name': data.get("pair_list")[index][loser].get("name")
				}

			print(f'{data.get("pair_list")[index][winner].get("name")}:{points_diff_winner}')
			print(f'{data.get("pair_list")[index][loser].get("name")}:{points_diff_loser}')

			index += 1

		print(Points)

		for song_id, items in Points.items():
			song = Song.objects.filter(song_id=song_id)
			if song:
				song = song[0]
				song.points = song.points + items.get("points")
				song.save(update_fields=['points'])
			else:
				song = Song(
					song_id = song_id,
					song_name = items.get("display_name"),
					points = items.get("points")
				)
				song.save()

		return Response({}, status=status.HTTP_200_OK)

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