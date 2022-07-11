from django.shortcuts import render, redirect
from .models import User
from spotify.utils import checkSpotifyAuthentication

# Template Rendering Views:
# TODO: Add Rankings view
def welcome(request):
	access_token = request.COOKIES.get('access_token')
	refresh_token = request.COOKIES.get('refresh_token')
	expires_in = request.COOKIES.get('expires_in')
	spotify_id = request.COOKIES.get('spotify_id')
	display_name = request.COOKIES.get('display_name')
	user_cover_image = request.COOKIES.get('user_cover_image')

	tokens = {
		'access_token': access_token,
		'refresh_token': refresh_token,
		'expires_in': expires_in
	}
	if(access_token != None and refresh_token != None and expires_in != None and spotify_id != None and display_name != None and user_cover_image != None):
		newTokens = checkSpotifyAuthentication(tokens)
		if(newTokens == None):
			pass
		else:
			access_token = newTokens.get('access_token')
			expires_in = newTokens.get('expires_in')

		# Increment no_of_visits in User model
		userProfile = User.objects.filter(spotify_id=spotify_id)
		if userProfile:
				userProfile = userProfile[0]
				userProfile.no_of_visits = userProfile.no_of_visits + 1
				userProfile.save(update_fields=['no_of_visits'])
		else:
			return render(request, 'app/welcome.html') 

		# Create cookies with token data:
		response = redirect('main-app:app-home')
		cookie_max_age = 365*24*60*60
		# Set Cookies
		response.set_cookie('access_token', access_token, cookie_max_age, samesite='Lax')
		response.set_cookie('refresh_token', refresh_token, cookie_max_age, samesite='Lax')
		response.set_cookie('expires_in', expires_in, cookie_max_age, samesite='Lax')
		response.set_cookie('spotify_id', spotify_id, cookie_max_age, samesite='Lax')
		response.set_cookie('display_name', display_name, cookie_max_age, samesite='Lax')
		response.set_cookie('user_cover_image', user_cover_image, cookie_max_age, samesite='Lax')
		
		return response
	else:
		return render(request, 'app/welcome.html') 

def home (request):
	return render(request, 'app/home.html')