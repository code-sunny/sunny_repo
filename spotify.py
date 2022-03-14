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

# 주어진 query에 대해 20곡의 노래를 받아 정보를 돌려보낸다.
def get_songs(query):
    response = sp.search(query, limit=20, type="track")
    items = response["tracks"]["items"]
    songs = []
    for track in items:
        song = {
            "track_id": track["id"],
            "artist": track["artists"][0]["name"],
            "title": track["name"],
            "preview_url": track["preview_url"],
            "cover_image": track["album"]["images"][1]["url"],
        }
        songs.append(song)
    return songs

# 트랙id를 기준으로 노래 정보를 돌려보낸다.
def get_track_info(track_id):
    track = sp.track(track_id)
    title = track["name"]
    artist = track["artists"][0]["name"]
    cover_image = track["album"]["images"][1]["url"]
    preview_url = track["preview_url"]
    return [title, artist, cover_image, preview_url]

