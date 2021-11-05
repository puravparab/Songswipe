from django.shortcuts import render, redirect
from spotify.utils import checkSpotifyAuthentication

# Template Rendering Views:
def welcome(request):
	access_token = request.COOKIES.get('access_token')
	refresh_token = request.COOKIES.get('refresh_token')
	expires_in = request.COOKIES.get('expires_in')

	tokens = {
		'access_token': access_token,
		'refresh_token': refresh_token,
		'expires_in': expires_in
	}
	if(access_token != None and refresh_token != None and expires_in != None):
		newTokens = checkSpotifyAuthentication(tokens)
		if(newTokens == None):
			pass
		else:
			access_token = newTokens.get('access_token')
			expires_in = newTokens.get('expires_in')

		# Create cookies with token data:
		response = redirect('main-app:app-home')
		cookie_max_age = 365*24*60*60
		# Set Cookies
		response.set_cookie('access_token', access_token, cookie_max_age, samesite='Lax')
		response.set_cookie('refresh_token', refresh_token, cookie_max_age, samesite='Lax')
		response.set_cookie('expires_in', expires_in, cookie_max_age, samesite='Lax')
		response.set_cookie('test', 'test', cookie_max_age, samesite='Lax')
		return response
	else:
		return render(request, 'app/welcome.html') 

def home (request):
	return render(request, 'app/home.html')