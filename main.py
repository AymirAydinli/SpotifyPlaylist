import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

load_dotenv()  # take environment variables from .env.

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

# date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

date = "2000-08-12"

print("https://www.billboard.com/charts/hot-100/" + date)

response = requests.get(f"https://www.billboard.com/charts/hot-100/" + date)

data = response.text

soup = BeautifulSoup(data, "html.parser")

song_list = soup.select(selector="li ul li h3")

songs = []

for item in song_list:
    song_name = item.getText().strip()
    songs.append(song_name)
print(songs)

# Spotify Login ______________________________________


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri="https://example.org/callback",
                              scope='playlist-modify-private'))

# Create a new playlist
playlist_name = 'My New Playlist'
user_id = sp.current_user()['id']  # Get the current user's Spotify ID
print(user_id)
# results = sp.search(q='weezer', limit=20)
# for idx, track in enumerate(results['tracks']['items']):
#     print(idx, track['name'])
