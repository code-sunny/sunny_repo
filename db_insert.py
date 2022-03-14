from unicodedata import name
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

# app1.py 임포트하여 함수를 불러오기
import app_hote

client = MongoClient("localhost", 27017)
db = client.dbsparta

# 트랙 id를 리스트로 리턴해줌
track_ids_list = app_hote.finding_trackId()


# db에 넣을 딕셔너리를 for문을 돌려서 하나씩 넣어주기
for i in track_ids_list:
    try:
        a = app_hote.giveout_etc(i)
        artist_name = a[0]
        title = a[1]
        preview_url = a[2]
        cover_image = a[3]

        doc = {
            f"title": "{title}",
            f"track_id": "{i}",
            f"artist": "{artist_name}",
            f"preview_url": "{preview_url}",
            f"cover_image": "{cover_image}",
            f"likes": {"Sunny": 0, "Snowy": 0, "Rainy": 0, "Cloudy": 0},
            f"likedUsers": [],
        }
        try:
            if preview_url == None:
                continue
            else:
                db.sings.insert_one(doc)
        except:
            continue

    except:
        continue
