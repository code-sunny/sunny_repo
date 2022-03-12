from dotenv import load_dotenv

load_dotenv()

import os

# BASE_LAT, BASE_LON은 위치정보가 받아지지 않았을 때를 위해 종로구의 좌표를 입력함
env_variables = {
    "port": os.getenv("PORT"),
    "lat": os.getenv("BASE_LAT"),
    "lon": os.getenv("BASE_LON"),
    "openweather_key": os.getenv("SERVICE_KEY"),
    "spotify_id": os.getenv("SPOTIFY_CLIENT_ID"),
    "spotify_secret": os.getenv("SPOTIFY_CLIENT_SECRET"),
}

from flask import Flask, jsonify, redirect, render_template, request, session
import requests

# import json
from pymongo import MongoClient

# session: 로그인 상태의 유지와 로그아웃 기능을 위해 필요
# session을 이용하여 로그인 된 유저가 새로고침을 했을 때 다시 로그인 하는 것을 방지하고
# 로그인 된 유저가 로그인/회원가입에 접근하는 것을 막을 수 있다.

# bcrypt: password를 암호화하고, 암호화된 password와 입력된 password를 비교하기 위한 라이브러리
# checkpw(비교할 암호, 저장된 암호) => True / False
# hashpw(해싱할 암호, 해싱횟수)
# gensalt 해싱횟수를 생성하기 위한 함수
# hashpw(해싱할 암호, gensalt())로 암호화할 수 있다.
from bcrypt import checkpw, hashpw, gensalt

db_client = MongoClient("localhost", 27017)
db = db_client.sunny

service_key = env_variables["openweather_key"]
base_lat = env_variables["lat"]
base_lon = env_variables["lon"]

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET")


@app.route("/")
def home():
    # ip주소를 따는 법
    # ip_address = request.remote_addr
    # print(session)
    return render_template("index.html")


@app.route("/j")
def j():
    return render_template("join.html")


@app.route("/main")
def main():
    return render_template("login.html")


@app.route("/join", methods=["POST"])
def join():
    # form에서 전송된 username과 password, password2
    if "username" in session:
        return redirect("/", 403)
    data = request.form
    username = data["username"]
    password = data["password"]
    password2 = data["password2"]
    # db에 username을 가진 유저를 찾는다.
    existing_user = db.users.find_one({"username": username})
    if existing_user:
        # db에 이미 존재하는 username일 경우
        return jsonify({"ok": False, "err": "이미 존재하는 사용자명입니다."})
    elif password != password2:
        # db에 존재하지 않으나 입력된 암호 둘이 동일하지 않을 경우
        return jsonify({"ok": False, "err": "패스워드가 동일하지 않습니다."})
    else:
        # db에 존재하지 않고, 암호가 일치 할 때
        # password를 암호화한다. hashpw(hashing 할 문자열, hashing 횟수)
        password = password.encode("utf-8")
        hashed_password = hashpw(password, gensalt())
        # db에 저장할 object 생성
        doc = {"username": username, "password": hashed_password}
        db.users.insert_one(doc)
        return redirect("/", 201)


@app.route("/login", methods=["POST"])
def login():
    if "username" in session:
        if session["username"]:
            return redirect("/", 403)
    data = request.form
    username = data["username"]
    password = data["password"]
    # db에서 username으로 검색
    user = db.users.find_one({"username": username})
    if not user:
        # 존재하지 않는 user
        return jsonify({"ok": False, "err": "존재하지 않는 사용자명입니다."})
    elif not checkpw(password.encode("utf-8"), user["password"]):
        # 입력된 password를 hash했을 때 저장된, hashing 된 password와 일치하지 않을 때
        return jsonify({"ok": False, "err": "잘못된 비밀번호입니다."})
    else:
        session["username"] = username
        # 로그인을 완료하고 첫 페이지로 돌아간다.
        return redirect("/", 200)


@app.route("/logout", methods=["GET"])
def logout():
    if not session["username"]:
        return redirect("/", 403)
    else:
        # session을 제거한다.
        session.clear()
        return redirect("/")


@app.route("/get-weather", methods=["POST"])
def weather_info():
    # frontend에서 json형식으로 보낸 위치정보를 받는다.
    pos = request.json
    lat = pos["lat"]
    lon = pos["lon"]
    print(pos)
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        # 위치정보를 요청할 parameters에 담는다.
        "lat": lat or base_lat,
        "lon": lon or base_lon,
        # 단위를 미터법에 맞게 받는다 (셀시우스)
        "units": "metric",
        # 날씨 정보를 우리말로 받는다. ex) "맑음", "구름" 등
        "lang": "kr",
        # openweather에 요청할 때 필요한 api_key를 담는다.
        "appid": service_key,
    }
    # requsets모듈을 - get method, url, params를 담아 요청
    response = requests.get(url, params=params)
    # 받은 response를 response.json()처리하여 json파일을 뽑고
    # weather 정보만 뽑아낸다
    weather = response.json()["weather"]
    # 뽑아낸 weather 정보를 frontend로 보낸다
    return jsonify({"weather": weather})


# , ssl_context="adhoc"
if __name__ == "__main__":
    app.run("0.0.0.0", env_variables["port"] or 3333, True)
