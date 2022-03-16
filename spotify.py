# from app import env_variables
from dotenv import load_dotenv

load_dotenv()
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from random import randint
import os
import pprint



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


def get_weather_song(keyword):
    try:
        search_limit = 30
        search = sp.search(q=keyword, limit=search_limit, type="playlist")

        playlist_id = search['playlists']['items'][0]['id']

        playlist_items_limit = 30
        playlist_items = sp.playlist_items(playlist_id=playlist_id, fields=None, limit=playlist_items_limit, offset=0, market='KR')


        songs_info = []
        for i in range(playlist_items_limit):
            song_info = playlist_items['items'][i]["track"]
            
            song_image_url = song_info['album']['images'][1]['url']
            song_name = song_info['name']
            song_preview_url = song_info['preview_url']
            song_artist = song_info["artists"][0]["name"]
            song_track_id = song_info['id']
            
            if song_preview_url != None:
                song = {
                    'title' : song_name,
                    'artist' : song_artist,
                    'track_id' : song_track_id,
                    'cover_image' : song_image_url,
                    'preview_url' : song_preview_url,
                    }
                
                songs_info.append(song)
    except:
        print(1)
            
    pprint.pprint(len(songs_info))
    
    return songs_info
        
def extract_10_songs():
    
    Sunny_list = get_weather_song("sunny")
    Cloudy_list = get_weather_song("cloudy")
    Rainy_list = get_weather_song("rainy")
    Snowy_list = get_weather_song("snowy")
    
    extract_Sunny_list = []
    extract_Cloudy_list = []
    extract_Rainy_list = []
    extract_Snowy_list = []
    
    cnt = 0
    while cnt <10:
        
        sunny_num = randint(0, len(Sunny_list)-1)
        extract_Sunny_list.append(Sunny_list.pop(sunny_num))
        
        cloudy_num = randint(0, len(Cloudy_list)-1)
        extract_Cloudy_list.append(Cloudy_list.pop(cloudy_num))
        
        rainy_num = randint(0, len(Rainy_list)-1)
        extract_Rainy_list.append(Rainy_list.pop(rainy_num))
        
        snowy_num = randint(0, len(Snowy_list)-1)
        extract_Snowy_list.append(Snowy_list.pop(snowy_num))
        
        cnt += 1
    
    return [extract_Sunny_list, extract_Cloudy_list, extract_Rainy_list, extract_Snowy_list]


