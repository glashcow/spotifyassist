from django.contrib import admin
from .models import *

admin.site.register(Artist)
admin.site.register(Track)
admin.site.register(Account)
admin.site.register(ArtistList)
admin.site.register(Playlist)