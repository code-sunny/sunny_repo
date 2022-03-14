from random import randint
from db import db
from spotify import get_songs

def song_recommend(weather):
    song = ""
    try:
        if db.songs.find({}, limit=1):
            song = db.songs.find({}, {"_id": False}).sort(f"likes.{weather}", -1)[0]
    except:
        num = randint(0, 19)
        song = get_songs(weather)[num]
        
    return song
    
def song_ranks(weather):
    songs = []
    
    try:
        if len(db.songs.find({}, limit=10)) >= 10:
            songs = db.songs.find({}, limit=10).sort(f"likes.{weather}", -1)
        elif len(db.songs.find({}, limit = 10)) > 0 and len(db.songs.find({}, limit=10)) < 10:
            songs.append(db.songs.find({}))
            songs.append(get_songs(weather)[0: 10-len(songs)])
    except:
        songs = get_songs(weather)[:10]
    
    return songs