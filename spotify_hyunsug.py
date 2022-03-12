# from app import env_variables
from dotenv import load_dotenv

load_dotenv()
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from youtube_hyunsug import get_youtube

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

auth_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret
)

sp = spotipy.Spotify(auth_manager=auth_manager)

# genres
# response = sp.recommendation_genre_seeds()["genres"]
# print(len(response), response)
# query = "아이유"
# search
# response = sp.search(query, limit=10, type="track")
# items = response["tracks"]["items"]


def get_songs(query_type, query):
    if query_type == "artist":
        query = "artist:" + query
    else:
        query = "track:" + query
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


toplists = sp.category_playlists("toplists", limit=1)["playlists"]["items"]
# toplists - playlists - items -> id
songs = []
for item in toplists:
    id = item["id"]
    tracks = sp.playlist_items(
        id,
        fields="items(track(id,album(artists,images),name,preview_url))",
        limit=1,
    )["items"]
    for track in tracks:
        track = track["track"]
        track_id = track["id"]
        track_artist = track["album"]["artists"][0]["name"]
        track_title = track["name"]
        track_image = track["album"]["images"][1]["url"]
        track_preview = track["preview_url"]
        track_youtube = get_youtube(track_artist + " " + track_title)
        track_info = {
            "id": track_id,
            "artist": track_artist,
            "title": track_title,
            "image": track_image,
            "preview": track_preview,
            "youtube": track_youtube,
        }
        songs.append(track_info)
