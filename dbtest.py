
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbplaylist

# 사용자가 버튼을 누른 곡 이름 : title_receive
title_receive = "eight";

# 사용자가 어떤 버튼을 눌렀는지 정보 : weather_receive
weatherBtn_receive = 'Sunny';

# 사용자가 누른 곡의 정보 조회해서 song에 저장
song = db.songs.find_one({'title':title_receive})

# if) 사용자가 누른 곡 이름이 db에 없다면, db에 default 값으로 추가 후
# 사용자가 누른 버튼에 맞게 수 +1
if (song == None):
    doc = {'title' : title_receive, 'Sunny' : 0, 'Cloudy' : 0, 'Rainy' : 0, 'Snowy' : 0}
    db.songs.insert_one(doc)
    song = db.songs.find_one({'title':title_receive})
    new_like = song[weatherBtn_receive] +1 
    db.songs.update_one({'title' : title_receive}, {'$set' : {weatherBtn_receive : new_like}})

# else) 이미 db에 곡 정보가 있다면 추가할 필요 없이 누른 버튼에 맞게 수 +1
else:
     new_like = song[weatherBtn_receive] +1 
     db.songs.update_one({'title' : title_receive}, {'$set' : {weatherBtn_receive : new_like}})