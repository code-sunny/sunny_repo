from dotenv import load_dotenv

from song_recommed import song_recommend, song_ranks
from spotify import get_songs

load_dotenv()

from env import env_variables

from flask import Flask, g, jsonify, redirect, render_template, request, session, url_for
from bcrypt import checkpw, hashpw, gensalt
from db import db
from weather import get_current_weather

app = Flask(__name__)
app.secret_key = env_variables["FLASK_SECRET"]

@app.before_request
def global_variables():
    g.title = "Mu:ther"

@app.route("/", methods=["GET"])
def landing_page():
    # random song 가져오기 -> 보내주기 구현
    # temp weather
    lat = env_variables["BASE_LAT"]
    lon = env_variables["BASE_LON"]
    current_weather, current_temp, current_city = get_current_weather(lat, lon)
    if "current_weather" in session:
        current_weather = session["current_weather"]
        current_temp = session["current_temp"]
        current_city = session["current_city"]
    song = song_recommend(current_weather)
    if "username" in session:
        return render_template("index.html", song=song, current_weather=current_weather, current_temp=current_temp, current_city=current_city, username=session["username"])
    return render_template("index.html", song=song, username="Guest")


@app.route("/about", methods=["GET"])
def about():
    if "username" in session:
        return render_template("aboutUs.html", username=session["username"])
    return render_template("aboutUs.html", username="Guest")


@app.route("/main", methods=["GET"])
def main_page():
    weather_to_show = request.args.get("weather")
    current_weather = session["current_weather"]
    current_temp = session["current_temp"]
    current_city = session["current_city"]
    songs_rank = song_ranks(current_weather)
    random_songs = get_songs(current_weather)
    username = "Guest"
    if username in session:
        username = session["username"]
    if weather_to_show is None:
        return render_template("sunny.html",username=username, random_songs=random_songs, songs_rank=songs_rank, current_city=current_city, current_weather=current_weather, current_temp=current_temp)
    else:
        songs_rank = song_ranks(weather_to_show)
        random_songs = get_songs(weather_to_show)
        return render_template("sunny.html",username=username, weather_to_show=weather_to_show, random_songs=random_songs,songs_rank=songs_rank, current_city=current_city, current_weather=current_weather, current_temp=current_temp)


@app.route("/main/search", methods=["GET"])
def search():
    query = request.args.get("query")
    username = "Guset"
    if "username" in session:
        username = session["username"]
    from spotify import get_songs

    songs = get_songs(query)
    return render_template("search.html", username=username, query=query, songs=songs)


@app.route("/main/song-rank", methods=["GET"])
def show_song_ranks():
    weatherToShow = request.args["moveBtn"]
    print(weatherToShow)
    song_rank = list(
        db.songs.find({}, {"_id": False}).sort(weatherToShow, -1).limit(10)
    )
    return jsonify({"songs_rank": song_rank})


@app.route("/api/show-like", methods=["GET"])
def show_song_likes():
    title_receive, artist_receive, username_receive = request.args.get()
    song = db.songs.find_one(
        {"title": title_receive, "artist": artist_receive}, {"_id": False}
    )
    return jsonify({"song_info": song})


@app.route("/api/like-btn", methods=["POST"])
def like():
    # 로그인 된 상태일 때
    if "username" in session:
        username = session["username"]
        # 트랙아이디, 날씨정보, 날씨에 눌린 좋아요 정보
        track_id, weather, weather_like_state = request.json.values()
        song = db.songs.find_one({"track_id": track_id})
        user = db.users.find_one({"username": username})
        # 노래가 존재하지 않을 떄
        if song is None:
            from spotify import get_track_info

            # 스포티파이api를 이용, 트랙의 타이틀, 가수명을 불러옴
            title, artist, cover_image, preview_url = get_track_info(track_id)
            # 신규 song 문서의 작성
            new_song = {
                "track_id": track_id,
                "title": title,
                "artist": artist,
                "cover_image": cover_image,
                "preview_url": preview_url,
                "likes": {
                    "Sunny": 0,
                    "Rainy": 0,
                    "Cloudy": 0,
                    "Snowy": 0,
                },
                "likedUsers": [],
            }
            likedUser = {
                "user": user["username"],
                "likes": {
                    "Sunny": False,
                    "Rainy": False,
                    "Cloudy": False,
                    "Snowy": False,
                },
            }
            likedUser["likes"][weather] = True
            new_song["likedUsers"].append(likedUser)
            new_song["likes"][weather] += 1
            clickedSong = {track_id: likedUser["likes"]}
            user["songs_liked"].append(clickedSong)
            db.users.update_one({"username": username}, {"$set": user})
            db.songs.insert_one(new_song)
            to_return = {"likes": new_song["likes"][weather]}
            return jsonify(to_return)
        else:
            to_update = f"likes.{weather}"
            count = song["likes"][weather]
            if weather_like_state is True:
                count = count - 1
                db.songs.update_one(
                    {"track_id": track_id}, {"$set": {to_update: count}}
                )
                db.users.update_one(
                    {"username": username}, {"$set": {f"likes.{weather}": False}}
                )
            else:
                count = count + 1
                db.songs.update_one(
                    {"track_id": track_id}, {"$set": {to_update: count}}
                )
                db.users.update_one(
                    {"username": username}, {"$set": {f"likes.{weather}": True}}
                )
        return jsonify({"likes": count})
    else:
        return redirect(url_for("/"), 403)


@app.route("/join", methods=["POST"])
def join():
    if "username" in session:
        return redirect(url_for("/"), 403)
    data = request.json
    username = data["username"]
    password = data["password"]
    password2 = data["password2"]
    existing_user = db.users.find_one({"username": username})
    if existing_user:
        return jsonify({"err": "이미 존재하는 사용자입니다."})
    elif password != password2:
        return jsonify({"err": "비밀번호가 일치하지 않습니다."})
    else:
        password = password.encode("utf-8")
        hashed_password = hashpw(password, gensalt())
        doc = {"username": username, "password": hashed_password, "songs_liked": []}
        db.users.insert_one(doc)
        return redirect("/", 201)


@app.route("/login", methods=["GET"])
def get_login():
    if "username" in session:
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    if "username" in session:
        if session["username"]:
            return redirect(url_for("/"), 403)
    data = request.json
    username = data["username"]
    password = data["password"]
    print(username, password)
    user = db.users.find_one({"username": username})
    if not user:
        return redirect("/login", 404)
    elif not checkpw(password.encode("utf-8"), user["password"]):
        return redirect("/login", 401)
    else:
        session["username"] = username
        return redirect("/", 200)


@app.route("/logout", methods=["GET"])
def logout():
    if not session["username"]:
        return redirect("/", 403)
    else:
        session.clear()
        return redirect("/")


@app.route("/user/my-profile")
def profile():
    if not "username" in session:
        return redirect("/", 403)
    else:
        return render_template("mypage.html", username=session["username"])

@app.route("/get-weather", methods=["POST"])
def get_weather():
    lat = env_variables["BASE_LAT"]
    lon = env_variables["BASE_LON"]
    if request.json:
        position = request.json
        lat = position["lat"]
        lon = position["lon"]

    weather, weather_temp, weather_city = get_current_weather(lat, lon)
    session["current_weather"] = weather;
    session["current_temp"] = weather_temp;
    session["current_city"] = weather_city;
    return jsonify({"weather": weather, "temp": weather_temp, "city": weather_city})

if __name__ == "__main__":
    app.run("0.0.0.0", env_variables["PORT"] or 5000, debug=True)
