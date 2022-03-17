from random import randint
from db import db
from spotify import extract_10_songs, get_songs
from random import randint

# 랜딩 페이지에 보내 줄 추천곡 하나를 위한 함수
def song_recommend(weather):
    song = ""
    try:
        # db에 노래가 존재한다면
        if db.songs.find({}, limit=1):
            # db에서 노래를 찾아 날씨 기준으로 정렬하여 가장 좋아요가 높은 곡을 보낸다.
            song = db.songs.find({}, {"_id": False}).sort(f"likes.{weather}", -1)[0]
    except:
        # db에 노래가 없다면
        # 20곡의 스포티파이 노래를 받아와 랜덤한 한 곡을 보낸다.
        weather_counter = 0
        if weather == "Cloudy":
            weather_counter = 1
        elif weather == "Rainy":
            weather_counter = 2
        elif weather == "Snowy":
            weather_counter = 3
        song = extract_10_songs()[weather_counter][0]
        
    return song

def song_ranks(weather):
    songs = [] or list(db.songs.find({}, {"_id": False}, limit=11).sort(f"likes.{weather}", -1))
    # db에 10곡 이상의 노래가 존재 시
    weather_counter = 0
    if weather == "Cloudy":
        weather_counter = 1
    elif weather == "Rainy":
        weather_counter = 2
    elif weather == "Snowy":
        weather_counter = 3
    if len(songs) >= 11:
        print("11+")
        ranks = list(db.songs.find({}, {"_id": False}).sort(f"likes.weather", -1))[:10]
        return ranks
    # db에 10곡 미만의 노래가 존재 시
    elif len(songs) > 0 and len(songs) < 10:
        spotify_songs = get_songs(weather)[0:10 - len(songs)]
        ranks = songs + spotify_songs
        return ranks
    # db에 노래가 없을 시
    else:
        return extract_10_songs()[weather_counter][:10]