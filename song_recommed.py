from random import randint
from db import db
from spotify import get_songs

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
        num = randint(0, 19)
        song = get_songs(weather)[num]
        
    return song

# random query generator?

# 메인 페이지에 좋아요 순으로 보여주기 위한 함수
def song_ranks(weather):
    songs = []
    
    try:
        # db에 10곡 이상의 노래가 존재 시
        if len(db.songs.find({}, limit=10)) >= 10:
            songs = db.songs.find({}, limit=10).sort(f"likes.{weather}", -1)
        # db에 10곡 미만의 노래가 존재 시
        elif len(db.songs.find({}, limit = 10)) > 0 and len(db.songs.find({}, limit=10)) < 10:
            songs.append(db.songs.find({}))
            songs.append(get_songs(weather)[0: 10-len(songs)])
    except:
        # db에 노래가 없을 시
        songs = get_songs(weather)[:10]
    
    return songs