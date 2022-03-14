from pymongo import MongoClient

# 그냥 app을 한 줄 더 줄이기 위한 db 분리
client = MongoClient("localhost", 27017)
db = client.sunny