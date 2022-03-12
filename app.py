# .env file loading
from dotenv import load_dotenv

load_dotenv()

# .env variables loading
import os

PORT = os.getenv("PORT")
BASE_LAT = os.getenv("BASE_LAT")
BASE_LON = os.getenv("BASE_LON")
OPENWEATHER_KEY = os.getenv("SERVICE_KEY")
SPOTIFY_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
FLASK_SECRET = os.getenv("APP_SECRET")


# flask server setting
from flask import Flask, jsonify, redirect, render_template, request, session

# from api import api
import requests

# 암호화용 library
from bcrypt import checkpw, hashpw, gensalt

from db import db

app = Flask(__name__)
# Blueprint를 이용하여, 단위별로 라우팅을 분리할 수 있다.
# app.register_blueprint(api)
# session 사용을 위해 flask가 secret key를 가져야 한다.
app.secret_key = FLASK_SECRET


@app.route("/", methods=["GET"])
def landing():
    if "username" in session:
        return render_template("index.html", {"username": session["username"]})
    return render_template("index.html")


@app.route("/main", methods=["GET"])
def main():
    if "username" in session:
        return render_template("main.html", {"username": session["username"]})
    return render_template("main.html")


@app.route("/main/search", methods=["GET"])
def search():
    # query = request.args.get()
    # from spotify import get_songs
    # songs = get_songs(query["query_type"], query["query"])
    return render_template("serach.html", {"result": []})


@app.route("/get-weather", methods=["POST"])
def get_weather():
    pos = request.json
    lat = pos["lat"]
    lon = pos["lon"]
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat or BASE_LAT,
        "lon": lon or BASE_LON,
        "units": "metric",
        "appid": OPENWEATHER_KEY,
    }
    response = requests.get(url, params=params)
    weather_id = response.json()["weather"]["id"]
    weather = ""
    if weather_id == 800:
        weather = "Sunny"
    elif weather_id >= 200 and weather_id < 600:
        weather = "Rainy"
    elif weather_id >= 600 and weather_id < 700:
        weather = "snowy"
    elif weather_id >= 700 and weather_id < 805:
        weather = "cloudy"
    return jsonify({"weather": weather})


@app.route("/join", methods=["POST"])
def join():
    # form에서 전송된 username과 password, password2
    if "username" in session:
        return redirect("/", 403)
    data = request.body.json()
    username = data["username"]
    password = data["password"]
    password2 = data["password2"]
    # db에 username을 가진 유저를 찾는다.
    existing_user = db.users.find_one({"username": username})
    if existing_user:
        # db에 이미 존재하는 username일 경우
        # return jsonify({"ok": False, "err": "이미 존재하는 사용자명입니다."})
        return redirect("/join", 400, {"error": "이미 존재하는 사용자명입니다."})
    elif password != password2:
        # db에 존재하지 않으나 입력된 암호 둘이 동일하지 않을 경우
        # return jsonify({"ok": False, "err": "패스워드가 동일하지 않습니다."})
        return redirect("/join", 400, {"error": "패스워드가 동일하지 않습니다."})
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
    data = request.body.json()
    username = data["username"]
    password = data["password"]
    # db에서 username으로 검색
    user = db.users.find_one({"username": username})
    if not user:
        # 존재하지 않는 user
        # return jsonify({"ok": False, "err": "존재하지 않는 사용자명입니다."})
        return redirect("/main", 400, {"error": "존재하지 않는 사용자명입니다."})
    elif not checkpw(password.encode("utf-8"), user["password"]):
        # 입력된 password를 hash했을 때 저장된, hashing 된 password와 일치하지 않을 때
        # return jsonify({"ok": False, "err": "잘못된 비밀번호입니다."})
        return redirect("/main", 400, {"error": "비밀번호가 일치하지 않습니다."})
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


# @app.route("/user/<userId>")로 하는 방법도 괜찮을 것 같다.
@app.route("/user/my-profile")
def profile():
    if not "username" in session:
        return redirect("/", 403)
    else:
        return render_template("/profile", {"username": session["username"]})


@app.route("/api/like-btn", methods=["POST"])
def new_like():
    if not "username" in session:
        return jsonify({"error": "로그인 되지 않은 이용자입니다."})
    else:
        query = request.args.get()
        song_id = query["song_id"]
        weather = query["weather"]

        return jsonify({"ok": True, "msg": "Like updated"})


@app.route("/api/show-like", methods=["GET"])
def show_like():
    args = request.args.get()
    track_id = args["track_id"]
    return None


@app.route("/api/song-info", methods=["GET"])
def song_info():
    song_info = {}
    return jsonify(song_info)


@app.route("/api/delete-like", methods=["DELETE"])
def delete_like():
    return None


if __name__ == "__main__":
    app.run("0.0.0.0", PORT or 5000, True)
