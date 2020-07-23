# Idea

This is a Django project that allows the user to generate "random" spotify playlists based on lists of musical artists that the user puts together, using Spotify's API. Using these lists, you generate a spotify list based on criteria such as:

  - Top tracks or deeper cuts from your artists
  - Either the artists themselves or their related artists
  - Number of tracks you would like to have in the playlist
 

# Files

### Python 
All python files are the standard Django project files. All the real work is in views.py where we have all the logic that generates the playlists and also deals with all the Javascript requests. Javascript deals with almost all the front end, populating the largly empty HTML files, so there are a number of functions in views that send JSON responses back to the JS for it to then show it as desired. Used crispy-forms so there's a forms.py file that deals with that.
### Models/db
In models.py there's a redundant Account model, however everything else is well used. When you add an arist to a list, views.py checks if that artist and their spoitfy id are stored in the DB, and stores them if they are not. This means that you don't have to talk to the spotify API everytime you add the artist to a list or generate a playlist. The same goes for any track you get when generating a playlist, even if you don't save that playlist. Using a simple local sqlite db, which is still only about 300kb despite the farily vast amount of artists and tracks that are in there.
### HTML/CSS/JS
As mentioned there are only a small number of HTML files and one CSS file which are controlled by Javascript. On most pages JS is adding elements with functions attatched to them, which is something I had never tried before. 

# Why It Meets the Criteria
 - This project shares the JS manipulation employed in the Pizza project, but to a larger extent. The JS is removing whole divs and replacing content AND talking to Django and getting JSON responses based on whatever it is you've requested. 
 - It also shares the API usage from the book shop project, but the spotify API is far more involved and we're doing a lot more with it and making exponentially more requests to it than the Goodreads.
 - It's a Django project, but compared to any other project the views.py is doing so much more. For one it's more than double the length of the pizza shop views.py, and despite the attempted refactoring, the logic is way more involved. I did a little bit of sweating over the playlist generation logic. 
 - Its also distinct in that it's not a generic "shop" project or a "normal" kind of website. Infact I intentionally didn't search for similar projects before I started so I wasn't influenced by them (obviously if this was a professional project I would have looked up similar sites/apps).
# Problems and Possible Improvements 
 - The UX isn't great, the philosophy I came in with was to keep things as simple as possible. However, the names of the different pages (e.g.) aren't great, initial users might be a little confused. For example you might think the "Generate Playlist" page takes you to a page where you can get the playlist out to spotify, whereas that would be "Export to Spotify", obvious when you think about it but not immediately evident.
 - It doesn't look wonderfully stylish, but that's just me not being overly interested in front-end. Also it being a backend heavy project I felt it pointless to take too much time making it look wonderful; it being a project in a online course and not made for the outside world. 
 - In retrospect I would have liked to Jsonify my artists and tracks, with a counter of how many playlists they appear in, and that's something I might look into.
 - The whole part where you have to copy the url into the console is actually deeply regrettable and I was due to hand this in about a month ago but keep coming back to try fix it but just can't. Well, I couldn't justify spending any more time fixing something for an online course.
 - There are a few bugs in the playlist generation that only arise in certain situations:
 -- Every artist only has 10 top tracks so if you ask for an 11 track playlist from the top tracks of one arists, you would get an index out of bounds excpetion (due to how the tracks are selected "randomly").
-- There's an issue where you can ask for tracks that don't exist, which happends when you want tracks from an album with some unavailable songs on it.
-- The small number of artists that have less than 10 tracks mess with the top track generation.
However all these things beig said, these problems could be solved fairly easily, however as stated for the puropses of the project this is already way more complex on the Python and JS sides than any of the other projects, so I believe sufficient. 