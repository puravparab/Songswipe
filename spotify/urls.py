"""spotify(songswipe) URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import *

app_name = 'spotify'

urlpatterns = [
    path('', welcome , name='spotify-index'),
    path('home', home, name='spotify-home'),
    path('authentication', AuthSpotify.as_view() , name='spotify-authentication'),
    path('callback', callback, name='spotify-callback'),

    # SPOTIFY APPLICATION API
    path('api/execute/', executeSpotifyAPIRequest.as_view(), name='spotify-api-execute'),
    path('api/user/', currentUserProfile, name='spotify-api-user'),
    path('api/user/saved-tracks/<int:limit>/<int:offset>/', userSavedTracks.as_view(), name='spotify-api-user-saved-tracks'),
    path('api/user/saved-tracks/check/', verifyTracksSaved.as_view(), name='spotify-api-user-saved-tracks-check'),
    path('api/user/saved-tracks/add/', addTracksToLibrary.as_view(), name='spotify-api-user-saved-tracks-add'),
]