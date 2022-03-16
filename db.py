from pymongo import MongoClient
from tracks import new_song, get_track_ids
from spotify import get_track_info

# db 설정
client = MongoClient('mongodb://--@0.0.0.0:27017')
db = client.sunny

# db에 하루에 한번씩 노래를 추가하는 코드
# import schedule
# import time

# def insert_songs():
#     track_ids = get_track_ids()
#     for track_id in track_ids:
#         if db.songs.find_one({"track_id": track_id}):
#             continue
#         else:
#             title, artist, cover_image, preview_url = get_track_info(track_id)
#             if preview_url is None:
#                 continue
#             else:
#                 song_doc = new_song(track_id, title, artist, preview_url, cover_image)
#                 db.songs.insert_one(song_doc)

# insert_songs()

# insert_songs()
# schedule.every(1).days.do(insert_songs)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
