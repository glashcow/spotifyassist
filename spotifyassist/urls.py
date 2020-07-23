from django.urls import path
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path("home/", views.index, name="index"),
    path("", views.open, name="open"),
    path("artistsearch/<str:searchvalue>", views.ArtistSearch, name="ArtistSearch"),
    path("artistslists/", views.ArtistLists, name="ArtistLists"),
    path("register/", views.register, name="register"),
    path("playlists/", views.playlists, name="playlists"),
    path("playlistlist/", views.playlistlist, name="playlistlist"),
    path("exportPlaylist", views.exportPlaylist, name="exportPlaylist"),
    path("viewplaylist/<str:playlistid>", views.viewplaylist, name="viewplaylist"),
    path("newplaylist/<str:artistlist>/<str:formartists>/<str:formtype>/<str:count>", views.newplaylist, name="newplaylist"),
    path("loadlist/<str:artistlist>", views.LoadList, name="LoadList"),
    path("newlist/<str:listname>", views.newlist, name="newlist"),
    path("makeplaylist/<str:uris>", views.makeplaylist, name="makeplaylist"),
    path("removeartist/<str:artistlist>/<str:artist>", views.removeartist, name="removeartist"),
    path("addtolist/<str:artistlist>/<str:artist>/<str:id>", views.addtolist, name="addtolist"),
    path('', include("django.contrib.auth.urls")),
]
