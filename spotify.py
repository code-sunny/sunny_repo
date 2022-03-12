# from app import env_variables
from dotenv import load_dotenv

load_dotenv()
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

auth_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret
)

sp = spotipy.Spotify(auth_manager=auth_manager)

# genres
# response = sp.recommendation_genre_seeds()["genres"]
# print(len(response), response)

# search
response = sp.search("artist:IU", limit=10, market="KR", type="track")
items = response["tracks"]["items"]

for item in items:
    artist = item["artists"][0]["name"]
    title = item["name"]
    print(title, "/ ", artist)
