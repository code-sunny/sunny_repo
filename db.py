from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.sunny

# db.create_collection("users")
# db.create_collection("songs")

# db.users.create_index("username", unique=True)

# example_user = {
#     "_id": "ObjectId",
#     "username": "username",
#     "password": "hashed_password",
#     "songs_liked": [
#         {
#             "song_id": "song_id",
#             "likes": {
#                 "Sunny": True,
#                 "Snowy": True,
#                 "Rainy": True,
#                 "Cloudy": True,
#             },
#         },
#     ],
# }
# example_song = {
#     "_id": "Objec tId('asdfasdfs')",
#     "title": "Song_title",
#     "track_id": "track_id",
#     "artist": "artist_name",
#     "likes": {"Sunny": 0, "Snowy": 1, "Rainy": 2, "Cloudy": 5},
#     "likedUsers": [
#         {
#             "userid": "userid",
#             "likes": {"Sunny": True, "Snowy": True, "Rainy": True, "Cloudy": True},
#         },
#         {
#             "userid": "userid",
#             "likes": {"Sunny": True, "Snowy": True, "Rainy": True, "Cloudy": True},
#         },
#     ],
# }
