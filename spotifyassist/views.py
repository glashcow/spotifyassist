import sys
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import json
from random import random

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

import tekore as tk

from .models import ArtistList, Artist, Track, Playlist
from .forms import RegisterForm

#requires setting client and secret environvars
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

spotify = tk.Spotify()
client_id = os.environ.get('SPOTIPY_CLIENT_ID')
client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
redirect_uri = 'http://127.0.0.1:8000'

#conf = tk.config_from_environment(return_refresh=True)
#client_id, client_secret, redirect_uri, user_refresh = conf
#cred = tk.Credentials(*conf)

#users = {}

def index(request):
    context = {
        "user" : request.user,
        "artistlists" : ArtistList.objects.filter(user=request.user)
    }
    return render(request, "spotifyassist/index.html", context)

def register(response):
    if response.method == "POST":
	    form = RegisterForm(response.POST)
	    if form.is_valid():
	        form.save()     
	    return HttpResponseRedirect(reverse("open"))
    else:
	    form = RegisterForm()
    return render(response, "spotifyassist/signup.html", {"form":form})     

def ArtistSearch(request, searchvalue):
    q = sp.search(q=searchvalue, type="artist", limit=5)["artists"]
    response_data = {}
    artists = []
    ids = []
    images = []
    for item in q["items"]:
        artists.append(item["name"])
        ids.append(item["id"])
        if item["images"] == []:
            string = "None"
            images.append(string)  
        else:
            images.append(item["images"][1]["url"])   
    response_data['artists'] = artists   
    response_data['ids'] = ids 
    response_data['images'] = images  
    return JsonResponse(response_data)

def open(request):
    return render(request, "spotifyassist/home.html")


@login_required
def ArtistLists(request):    
    context = {
        "user" : request.user,
        "artistlists" : ArtistList.objects.filter(user=request.user),
        "artists" : Artist.objects.all()
    }
    return render(request, "spotifyassist/artistlist.html", context)

@login_required
def playlists(request):
    context = {
        "user" : request.user,
        "artistlists" : ArtistList.objects.filter(user=request.user),
    }
    return render(request, "spotifyassist/playlistmaker.html", context)


def addtolist(request, artistlist, artist, id):
    artistlist = ArtistList.objects.filter(user=request.user).filter(list_name=artistlist).first()
    if(ArtistIsNotInDb(id)):
        artist = Artist(name=artist, spotify_id=id)
        artist.save()
    artistForList = Artist.objects.get(spotify_id=id)
    if(ArtistIsAlreadyInList(artistlist, id)):
        return JsonResponse({"message" : "Artist Already In List"})
    else:
        artistlist.artists.add(artistForList)
        artistlist.save()
        return JsonResponse({"message" : "Added to List"})   

def ArtistIsNotInDb(id):
    q = Artist.objects.filter(spotify_id=id)  
    return not q.exists()


def ArtistIsAlreadyInList(artistlist, id):
    alreadyin = False
    for artist in artistlist.artists.all():
        if artist.spotify_id == id:
            alreadyin = True
    return alreadyin        

def LoadList(request, artistlist):
    listToLoad = ArtistList.objects.filter(list_name=artistlist).filter(user=request.user).first()
    artists = []
    for artist in listToLoad.artists.all():
        artists.append(artist.name)
    return JsonResponse({"artists" : artists })     

def newplaylist(request, artistlist, formartists, formtype, count):
    artists = getArtistIdsFromList(request, artistlist)
    count = int(count)    
    numberofartists = len(artists)
    tracksperartist = int(count/numberofartists)
    remainder = count%numberofartists
    if formtype == "toptracks":
        return topTrackPlaylist(request, artists, formartists, count,  tracksperartist, remainder)
    else:
        return deeperCutsPlaylist(request, artists, formartists, count,  tracksperartist, remainder)

def topTrackPlaylist(request, artists, formartists, count,  tracksperartist, remainder):
    tracks = []
    response_data = {}
    if formartists == "inlist":
        for ids in artists:
            q = sp.artist_top_tracks(ids, country="GB")
            indeces = []
            for i in range(10):
                indeces.append(i)
            add = remainderadd(remainder)    
            for i in range(tracksperartist + add):
                randomrange = 10 - i
                index = int(random() * randomrange)
                track_id = q["tracks"][indeces[index]]["id"]
                title = q["tracks"][indeces[index]]["name"]
                artist_id = ids
                checkTrackIsInDb(track_id, title, artist_id)
                track = Track.objects.filter(spotify_id = track_id).first()
                tracks.append(track)
                del indeces[index]
            remainder -= 1       
    elif formartists == "insimilar":
        for ids in artists:
            q = sp.artist_related_artists(ids) 
            add = remainderadd(remainder)    
            for i in range(tracksperartist + add):
                index = int(random() * 7)
                artist_id = q["artists"][index]["id"]
                artist_name = q["artists"][index]["name"]
                checkArtistsInDb(artist_id, artist_name)
                index2 = int(random() * 5)
                q2 = sp.artist_top_tracks(artist_id)["tracks"][index2]
                track_id = q2["id"]
                title = q2["name"]
                checkTrackIsInDb(track_id, title, artist_id)
                track = Track.objects.filter(spotify_id = track_id).first()
                tracks.append(track)
            remainder -= 1    
    derangedtracks = derangelist(tracks)        
    trackstrings = []
    uris = []
    for track in derangedtracks:
        trackstrings.append(str(track))   
    for track in derangedtracks:
        uris.append(track.spotify_id)  
    response_data["uris"] = uris        
    response_data["tracks"] = trackstrings    
    return JsonResponse(response_data)

def remainderadd(remainder):
    if remainder > 0:
        add = 1
    else:
        add = 0    
    return add

def deeperCutsPlaylist(request, artists, formartists, count, tracksperartist, remainder):
    tracks = []
    response_data = {} 
    if formartists == "inlist":
        for ids in artists:
            artist = Artist.objects.filter(spotify_id=ids).first()
            albumlist = []
            q = sp.artist_albums(ids, country="GB")["items"]
            for i in range(len(q)):
                name = q[i]["artists"][0]["name"] 
                if name == artist.name:
                    albumlist.append(q[i])
            albumsbyartist = len(albumlist)
            add = remainderadd(remainder)  
            for j in range(tracksperartist + add):
                randomalbumindex = int(random() * albumsbyartist)
                album_id = albumlist[randomalbumindex]["id"]
                album = sp.album(album_id)
                nooftracks = album["total_tracks"]
                trackindex = int(random() * nooftracks)
                track_name = album["tracks"]["items"][trackindex]["name"]
                track_id = album["tracks"]["items"][trackindex]["id"]
                checkTrackIsInDb(track_id, track_name, ids)
                track = Track.objects.filter(spotify_id = track_id).first()
                tracks.append(track)
            remainder -= 1    
    else:
        for ids in artists:
            q = sp.artist_related_artists(ids)
            add = remainderadd(remainder)
            for i in range(tracksperartist + add):
                index = int(random() * 7)
                artist_id = q["artists"][index]["id"]
                artist_name = q["artists"][index]["name"]
                checkArtistsInDb(artist_id, artist_name)    
                artist = Artist.objects.filter(spotify_id=artist_id).first()
                albumlist = []
                q2 = sp.artist_albums(artist_id, country="GB")["items"]
                for i in range(len(q2)):
                    name = q2[i]["artists"][0]["name"] 
                    if name == artist.name:
                        albumlist.append(q2[i])        
                albumsbyartist = len(albumlist)
                randomalbumindex = int(random() * albumsbyartist)
                album_id = albumlist[randomalbumindex]["id"]
                album = sp.album(album_id)
                nooftracks = album["total_tracks"]
                trackindex = int(random() * nooftracks)
                track_name = album["tracks"]["items"][trackindex]["name"]
                track_id = album["tracks"]["items"][trackindex]["id"]
                checkTrackIsInDb(track_id, track_name, artist_id)
                track = Track.objects.filter(spotify_id = track_id).first()
                tracks.append(track)
            remainder -= 1     
    derangedtracks = derangelist(tracks)        
    trackstrings = []
    uris = []
    for track in derangedtracks:
        trackstrings.append(str(track))     
    for track in derangedtracks:
        uris.append(track.spotify_id)  
    response_data["uris"] = uris    
    response_data["tracks"] = trackstrings         
    return JsonResponse(response_data)           

def getArtistIdsFromList(request, artistlist):
    listtouse = ArtistList.objects.filter(list_name=artistlist).filter(user=request.user).first()
    artists = []
    for artist in listtouse.artists.all():
        artists.append(artist.spotify_id)
    return artists    

def checkTrackIsInDb(track_id, title, artist_id):
    q = Track.objects.filter(spotify_id=track_id)
    if not q.exists():
        artist = Artist.objects.filter(spotify_id = artist_id).first()
        track = Track(title = title, artist = artist, spotify_id = track_id )
        track.save()
    else:
        pass

def checkArtistsInDb(artist_id, name):
    q = Artist.objects.filter(spotify_id=artist_id)
    if not q.exists():
        artist = Artist(name = name, spotify_id=artist_id)
        artist.save()
    else:
        pass

def derangelist(alist):
    outlist = []
    indeces = []
    length = len(alist)
    for i in range(length):
        indeces.append(i)
    for j in range(length):
        randomrange = length - j
        index = int(random() * randomrange)  
        outlist.append(alist[index])   
        del alist[index]
    return outlist    

def removeartist(request, artistlist, artist):
    thelist = ArtistList.objects.filter(list_name=artistlist).filter(user=request.user).first()
    theartist = Artist.objects.filter(name=artist).first()
    thelist.artists.remove(theartist)
    artists = thelist.artists.all()
    returnlist = []
    for artist in artists:
        returnlist.append(artist.name)
    return JsonResponse({"artists" : returnlist})

def newlist(request, listname):
    print(listname)
    lists = ArtistList.objects.filter(user=request.user).all()
    response_data = {}
    alreadyexists = False
    for _list in lists:
        if _list.list_name == listname:
            alreadyexists = True
            break
    if alreadyexists:
        message = "That list Already exists"
        good = "bad"
    else:
        message = "New List Created"
        newlist = ArtistList(list_name = listname, user = request.user) 
        newlist.save()
        good = "good"
    response_data["message"] = message
    response_data["good"] = good  
    return JsonResponse(response_data)

def makeplaylist(request, uris):
    ids = uris.split(",")
    playlistcount = Playlist.objects.filter(user=request.user).count() + 1
    playlist = Playlist(user = request.user, name = f"New Playlist {playlistcount}")
    playlist.save()
    playlist = Playlist.objects.filter(user=request.user).last()
    for _id in ids:
        track = Track.objects.filter(spotify_id = _id).first()
        playlist.tracks.add(track)
    return JsonResponse({"message" : "Playlist Added"})

def playlistlist(request):
    context = {
        "playlists" : Playlist.objects.filter(user = request.user).all()
    }
    return render(request,"spotifyassist/playlists.html", context)

def viewplaylist(request, playlistid):
    playlist = Playlist.objects.get(id=playlistid)
    tracks = []
    for track in playlist.tracks.all():
        tracks.append(str(track))
    context = {
        "playlistid" : playlistid,
        "tracks" : tracks
    }  
    return render(request, "spotifyassist/playlistview.html", context)

def exportPlaylist(request):
    list_id = request.POST["playlilstid"] 
    playlisttoexport = Playlist.objects.get(id=list_id)
    tracks = playlisttoexport.tracks.all()
    uris = []
    for t in tracks:
        uri = "spotify:track:" + t.spotify_id
        uris.append(uri)
    app_token = tk.request_client_token(client_id, client_secret)
    spotify = tk.Spotify(app_token)
    user_token = tk.prompt_for_user_token(
        client_id,
        client_secret,
        redirect_uri,
        scope=tk.scope.every
    )
    spotify.token = user_token
    user = spotify.current_user()
    playlist = spotify.playlist_create(
        user.id,
        playlisttoexport.name,
        public=False,
        description='Generated By Ewan\'s Spotify Playlist Assist'
    ) 
    spotify.playlist_add(playlist.id, uris=uris)


    #THIS IS WHERE ONE AVIODS COPYING PASTING INTO COSNOLE, COULDN'T QUITE WORK IT, FOR THE PURPOSES OF THIS PROJECT I DECIDED TO NOT WASTE MORE TIME ON IT

    #code = request.GET.get('', '')
    #token = cred.request_user_token(code)
    #with spotify.token_as(token):
    #    info = spotify.current_user()
    #    session['user'] = info.id
    #    users[info.id] = token


    return HttpResponseRedirect(reverse("playlistlist"))



