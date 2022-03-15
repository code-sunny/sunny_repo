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




def get_category():
    # 카테고리를 분류한다.
    cate_count = 50
    cate = sp.categories(country='KR', locale=None, limit=cate_count, offset=0)

    cate_ids = []
    # 카테고리 수만큼 반복
    for i in range(40):
        # 카테고리 아이디 저장(party, pop, ...)
        cate_id = cate["categories"]["items"][i]['id']
        # 카테고리 아이디 시작이 문자면 cate_ids에 추가
        # 아이디가 아니라 숫자면 items가 빈 값이 나와서 제외
        if cate_id[0].isalpha():
            cate_ids.append(cate_id)         

    return cate_ids

def get_features(song): 
    try:
        # track id 정보
        track_info = sp.search(q=song, type='track') 
        track_id = track_info["tracks"]["items"][0]["id"] 
        
        # get audio_feature 
        features = sp.audio_features(tracks=[track_id]) 
        energy = features[0]["energy"] 
        valence = features[0]["valence"] 
        tempo = features[0]["tempo"]
        # danceability : 춤 추기 적합 정도
        # energy : 에너지 정도, 빠르고, 화려하고 노이즈 많을수록 값 크다
        # mode : 장조 - 1 / 단조 - 0
        # tempo : BPM
        # valence : 음원의 밝음 정도 - 밝고, 행복하면 값 높고, 우울하면 값 낮다.
        result = { 
                "energy" : energy,  
                "valence" : valence, 
                "tempo" : tempo,
                } 
    except:
        return 
    return result


def get_random_songs():
    cate_ids = get_category()
    songs_info = []
    for i in range(len(cate_ids)):  
        try:
            cate_playlist_limit = 2
            cate_playlist = sp.category_playlists( category_id= cate_ids[i], country='KR', limit=cate_playlist_limit, offset=0 )
            
            # 플레이리스트 id를 찾을 수 있을 때만 실행
            if len(cate_playlist["playlists"]) != 0:
                for i in range(cate_playlist_limit):
                    playlist_id = cate_playlist["playlists"]["items"][i]['id']
                    
                    playlist_items_limit = 4
                    playlist_items = sp.playlist_items(playlist_id=playlist_id, fields=None, limit=playlist_items_limit, offset=0, market=None)
                    
                    for j in range(playlist_items_limit):
                        song_info = playlist_items["items"][j]["track"]
                        
                        song_name = song_info['name']
                        song_preview_url = song_info['preview_url']
                        song_artist = song_info["artists"][0]["name"]
                        
                        features = get_features(song_name)
                        energy = features['energy']
                        valence = features['valence']
                        tempo = features['tempo']
                        
                        if song_preview_url != None:    
                            song = {
                                'name' : song_name,
                                'preview_url' : song_preview_url,
                                'artist' : song_artist,
                                'features' : {
                                    'energy' : energy,
                                    'valence' : valence,
                                    'tempo' : tempo
                                }
                            }
                    
                            songs_info.append(song)
                                                         
        except:
            continue
        
    return songs_info



def classify_song():
    
    Sunny_list = []
    Cloudy_list = []
    Rainy_list = []
    Snowy_list = []
    
    origin_song = get_random_songs()
    for i in range(len(origin_song)):
        energy = origin_song[i]['features']['energy']
        valence = origin_song[i]['features']['valence']
        tempo = origin_song[i]['features']['tempo']

        if energy > 0.8:
            Sunny_list.append(origin_song[i])
        
        if (energy < 0.65) and (valence < 0.4) and (tempo < 100):
            Cloudy_list.append(origin_song[i])

        if (energy < 0.65) and (valence < 0.4) and (tempo < 100):
            Rainy_list.append(origin_song[i])
            
        if (0.65 <= energy <= 0.8) and (valence > 0.5) and (tempo > 70):
            Snowy_list.append(origin_song[i])
    
    # 날씨별 곡 수 확인용         
    # print(len(Sunny_list), len(Cloudy_list), len(Rainy_list), len(Snowy_list))    
            
    return [Sunny_list, Cloudy_list, Rainy_list, Snowy_list]

def extract_10_song():
    song_list = classify_song()
    Sunny_list = song_list[0]
    Cloudy_list = song_list[1]
    Rainy_list = song_list[2]
    Snowy_list = song_list[3]
    
    extract_Sunny_list = []
    extract_Cloudy_list = []
    extract_Rainy_list = []
    extract_Snowy_list = []
    
    cnt = 0 
    while cnt < 10:
        num = randint(0, len(Sunny_list)-1)
        extract_Sunny_list.append(Sunny_list.pop(num))
        cnt += 1
        
    print(extract_Sunny_list)
    
extract_10_song()