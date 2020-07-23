from django.test import TestCase
from .views import *
from .models import *


class ModelsTestCase(TestCase):

    def setUp(self):
        artist1 = Artist.objects.create(name="Fake Artist", spotify_id="abcdefg")

    def test_artist_object_creation(self):
        a = Artist.objects.get(name="Fake Artist")
        self.assertEquals(a.name, "Fake Artist")

    def check_artist_in_db_fuction(self):
        self.assertTrue(ArtistIsNotInDb("12345"))

    def negative_check_artist_in_db_fuction(self):
        self.assertFalse(ArtistIsNotInDb("abcdefg"))

    