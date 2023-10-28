import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

load_dotenv()  # take environment variables from .env.

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

data = response.text

soup = BeautifulSoup(data, "html.parser")

songs = soup.find_all(name="h3", id="title-of-a-story", class_="u-line-height-125")

song_titles = [title.getText().strip("\n\t") for title in songs]

artists = soup.find_all(name="span", class_="u-max-width-330")

artist_names = [name.getText().strip("\n\t") for name in artists]

song_and_artist = dict(zip(song_titles, artist_names))

print(song_and_artist)
print()
print("Searching for songs on Spotify and creating new playlist...")

# Spotify Login and Search ______________________________________


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                              redirect_uri="https://example.org/callback",
                              scope='playlist-modify-private'))

song_uris = []

for (song, artist) in song_and_artist.items():
    try:
        print(song, artist)
        result = sp.search(q=f"track:{song} artist:{artist}", type="track")
        uri = result["tracks"]["items"][0]['uri']
        song_uris.append(uri)
    except:
        print(f"{song} by {artist} does not exist in spotify")
        pass

print(f"Number of songs found: {len(song_uris)}")

# Create a new private playlist in Spotify

user_id = sp.current_user()['id']

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Bilboard 100", public=False)

print(playlist)

# Add songs into the playlist
sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris)



print(f"New playlist '{date} Billboard 100' successfully created on Spotify!")
