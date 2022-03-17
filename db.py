from pymongo import MongoClient
# db 설정
# dev
client = MongoClient("localhost", 27017)
# production
# client = MongoClient('mongodb://@0.0.0.0:27017')
db = client.sunny
