from dotenv import load_dotenv
load_dotenv()

from env import env_variables
from song_recommed import song_recommend, song_ranks
from spotify import get_songs, get_track_info, extract_10_songs 


from flask import Flask, g, jsonify, redirect, render_template, request, session, url_for
from bcrypt import checkpw, hashpw, gensalt
from db import db
from weather import get_current_weather

app = Flask(__name__)
app.secret_key = env_variables["FLASK_SECRET"]

@app.before_request
def global_variables():
    # flask 전체에 공유되는 변수를 설정한다. (global variables)
    g.title = "Mu:ther"

@app.after_request
def after_request(response):
    return response

@app.route("/", methods=["GET"])
def landing_page():
    # random song 가져오기 -> 보내주기 구현
    # 기본날씨 서울 종로구 기준 부여
    lat = env_variables["BASE_LAT"]
    lon = env_variables["BASE_LON"]
    # get_current_weather를 통해 날씨, 기온, 도시 이름을 받아옴
    current_weather, current_temp, current_city = "", "", ""
    if "current_weather" in session:
        # get-weather가 실행되면 session에 위의 세 정보가 실제 정보로 저장된다.
        current_weather = session["current_weather"]
        current_temp = session["current_temp"]
        current_city = session["current_city"]
    else:
        current_weather, current_temp, current_city = get_current_weather(lat, lon)
    # landing page에 보내질 노래 정보를 db를 우선하여, 없을 시 스포티파이 api를 이용하여 받아온다. 
    song = song_recommend(current_weather)
    # 로그인된 상태라면 로그인된 유저네임을, 아닐 시 유저네임을 Guest로 설정하여 보낸다.
    if "username" in session:
        return render_template("index.html", song=song, current_weather=current_weather, current_temp=current_temp, current_city=current_city, username=session["username"])
    else:
        return render_template("index.html", song=song, current_weather=current_weather, current_temp=current_temp, current_city=current_city, username="Guest")


@app.route("/about", methods=["GET"])
def about():
    if "username" in session:
        return render_template("aboutUs.html", username=session["username"])
    return render_template("aboutUs.html", username="Guest")


@app.route("/main", methods=["GET"])
def main_page():

    
    # main에 접속함은 랜딩 페이지에서 넘어온 상태이므로 세션에 날씨 정보들이 들어있다.
    # main에 바로 접근 하는 것을 막는다.
    if "current_weather" not in session:
        return redirect("/")
    # main page에 있는 날씨 버튼을 누를 시 아래의 weather_to_show가 받아와진다
    weather_to_show = request.args.get("weather")
    current_weather = session["current_weather"]
    current_temp = session["current_temp"]
    current_city = session["current_city"]
    # 랭크 섹션에 전달할 노래들을 받아온다 -> DB 우선, 없을 시 스포티파이
    songs_rank = song_ranks(current_weather)
    # 랜덤 섹션에 전달할 노래들을 받아온다 -> 스포티파이
    weather_counter = 0
    if weather_to_show == "Cloudy":
        weather_counter = 1
    elif weather_to_show == "Rainy":
        weather_counter = 2
    elif weather_to_show == "Snowy":
        weather_counter = 3
    songs_random = extract_10_songs()[weather_counter]
    # 기본 사용자명을 게스트로 설정하고 로그인된 상태라면 로그인 유저네임으로 변경한다.
    
    username = "Guest"
    if username in session:
        username = session["username"]
    if weather_to_show is None:
        return render_template("sunny.html",username=username, random_songs=songs_random, songs_rank=songs_rank, current_city=current_city, current_weather=current_weather, current_temp=current_temp)
    else:
        songs_rank = song_ranks(weather_to_show)
        return render_template("sunny.html",username=username, weather_to_show=weather_to_show, random_songs=songs_random, songs_rank=songs_rank, current_city=current_city, current_weather=current_weather, current_temp=current_temp)


@app.route("/main/search", methods=["GET"])
def search():
    # search 페이지로 접근 시 검색어를 query로 받아온다
    query = request.args.get("query")
    
        # random song 가져오기 -> 보내주기 구현
    # 기본날씨 서울 종로구 기준 부여
    lat = env_variables["BASE_LAT"]
    lon = env_variables["BASE_LON"]
    # get_current_weather를 통해 날씨, 기온, 도시 이름을 받아옴
    current_weather, current_temp, current_city = "", "", ""
    if "current_weather" in session:
        # get-weather가 실행되면 session에 위의 세 정보가 실제 정보로 저장된다.
        current_weather = session["current_weather"]
        current_temp = session["current_temp"]
        current_city = session["current_city"]
    else:
        current_weather, current_temp, current_city = get_current_weather(lat, lon)
    
    # 사용자명 설정
    username = "Guest"
    if "username" in session:
        username = session["username"]
    from spotify import get_songs
    # 스포티파이에서 검색하여 받아온 노래정보를 넘겨 렌더링한다.
    songs = get_songs(query)
    return render_template("search.html", username=username, query=query, songs=songs, current_city=current_city, current_weather=current_weather, current_temp=current_temp)

# 이 부분은 안 쓰게 될 것 같다.
@app.route("/main/song-rank", methods=["GET"])
def show_song_ranks():
    weatherToShow = request.args["moveBtn"]

    song_rank = list(
        db.songs.find({}, {"_id": False}).sort(weatherToShow, -1).limit(10)
    )
    return jsonify({"songs_rank": song_rank})

# 수정 중
@app.route("/api/show-like", methods=["GET"])
def show_song_likes():
    title_receive  = request.args["title_receive"]
    artist_receive = request.args["artist_receive"]
    username_receive = request.args["username_receive"]
    song = db.songs.find_one(
        {"title": title_receive, "artist": artist_receive, "username": username_receive}, {"_id": False}
    )
    return jsonify({"song_info": song})


# 작업 중
@app.route("/api/like-btn", methods=["POST"])
def like():
    
    # 로그인 된 상태일 때
    if "username" in session:
        username = session["username"]
        # 트랙아이디, 날씨정보, 날씨에 눌린 좋아요 정보
        track_id, weather = request.json.values()
        song = db.songs.find_one({"track_id": track_id})
        user = db.users.find_one({"username": username})
        print("****************")
        print(song)
        # 노래가 존재하지 않을 떄
        if song is None:
            
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
            # 좋아요를 누른 사용자
            likedUser = {
                username: {
                    "Sunny": False,
                    "Rainy": False,
                    "Cloudy": False,
                    "Snowy": False,
                },
            }
            # 사용자 -> 좋아요 -> 해당 날씨 True
            likedUser[username][weather] = True
            # 새 노래 -> 사용자들 -> 현재 사용자 추가
            new_song["likedUsers"].append(likedUser)
            # 새 노래 해당 날씨의 좋아요 = 1 (최초니까)
            new_song["likes"][weather] = 1
            # 사용자가 좋아요를 누른 곡 목록에 위 내용을 더한다
            user["songs_liked"][track_id] = likedUser[username]
            # 사용자를 업데이트한다. 
            db.users.update_one({"username": username}, {"$set": {"songs_liked": user["songs_liked"]}})
            # 신규 노래 삽입
            db.songs.insert_one(new_song)
            # 신규 음악의 좋아요 갯수를 돌려보낸다. (받을 곳이 없어 의미는 크게 없는 듯)
            to_return = {"likes": new_song["likes"][weather]}
            return jsonify(to_return)
        # 노래가 DB에 존재할 때
        else:
            # 업데이트해야 하는 날씨
            to_update = f"likes.{weather}"
            # 유저가 해당 곡에 좋아요를 눌렀던 적이 있는 경우
            if track_id in user["songs_liked"]:
                # 좋아요를 누른 적도 있고, 해당 날씨에 좋아요를 누른 곡인 경우
                
                if user["songs_liked"][track_id][weather]:
                    db.songs.update_one(
                        {"track_id": track_id}, {"$inc": {to_update: -1}}
                    )
                    user_liked = user["songs_liked"]

                    user_liked[track_id][weather] = False
    
                    db.users.update_one(
                        {"username": username}, {"$set": {"songs_liked": user_liked}}
                    )
                    return jsonify({"msg": "TEST"})
                # 좋아요를 누른 적은 있지만 해당 날씨는 아닌 경우
                else:
                    db.songs.update_one(
                        {"track_id": track_id}, {"$inc": {to_update: 1}}
                    )
                    user_liked = user["songs_liked"]                    
   
                    user_liked[track_id][weather] = True

                    db.users.update_one(
                        {"username": username}, {"$set": {"songs_liked": user_liked}}
                    )
                    return jsonify({"msg": "TEST"})
            # 유저가 해당 곡에 좋아요를 눌렀던 적이 없는 경우
            else:
                #유저가 해당 곡과 상호작용을 한 적이 없고 db에 노래가 있는 경우
                # 날씨 상태가 False일 수 밖에 없다.
                db.songs.update_one(
                    {"track_id": track_id}, {"$inc": {to_update: 1}}
                )
                likedUser = {
                    username: {
                        "Sunny": False,
                        "Rainy": False,
                        "Cloudy": False,
                        "Snowy": False,
                    },
                }
                likedUser[username][weather] = True
                db.songs.update_one(
                    {"track_id": track_id}, {"$addToSet": {"likedUsers": likedUser}}
                )
                # 해당 날씨를 업데이트한다.
                user["songs_liked"][track_id] = {
                    "Sunny": False,
                    "Rainy": False,
                    "Cloudy": False,
                    "Snowy": False,
                }    
                user["songs_liked"][track_id][weather] = True
                db.users.update_one(
                    {"username": username}, {"$set": {"songs_liked": user["songs_liked"]}}
                )
        return jsonify({"msg": "Likes updated!"})
    
    # 로그인 되지 않았으면 로그인 페이지로 redirect
    else:
        return jsonify({'msg' : "먼저 로그인 해주세요!", 'redirect_url' : "/login"})
  

@app.route("/api/song-info", methods=["GET"])
def show_song_info():
    song_list = extract_10_songs()
    return jsonify({"song_list": song_list})


@app.route("/api/delete-like", methods=["DELETE"])
def delete_like():
    if "username" not in session:
        return redirect("/")
    else:
        # 받아온 트랙아이디, 좋아요가 눌려있는 날씨
        track_id, weather = request.json.values()
        username = session["username"]
        likes = list(db.songs.find({"track_id": track_id}, {"_id": False}))[0]

        
        song = db.songs.find({"track_id": track_id}, {"_id": False})
        user = db.users.find({"username": username}, {"_id": False})
        likedUsers = list(song)[0]["likedUsers"]
        toUpdate = []
        x = 0
        for i in range(len(likedUsers)):
            if likedUsers[i][username]:
                x = i
                toUpdate = likedUsers[x]
                break
            else:
                continue
        toUpdate[username][weather] = False
        db.songs.update_one({"track_id": track_id}, {"$set": {"likedUsers": likedUsers}})

        # 좋아요 수가 0 밑으로 간다면
        if likes['likes'][weather]-1 >= 0:
            db.songs.update_one({"track_id": track_id}, {"$inc": {f"likes.{weather}": -1}})
        else:
            return jsonify({"ok": False, 'msg' : "이미 삭제된 곡입니다!"})
        
        songs_liked = list(user)[0]["songs_liked"]
        # print(songs_liked)
        songs_liked[track_id][weather] = False
        db.users.update_one({"username": username}, {"$set": {"songs_liked": songs_liked}})
                
        return jsonify({"ok": True, "msg": "삭제되었습니다."})
    

    
        



@app.route("/join", methods=["POST"])
def join():
    # 로그인 된 상태일 시 돌려보낸다.
    if "username" in session:
        return redirect("/")
    # json 형태로 전달된 회원가입 정보를 data로 받는다
    data = request.json
    username = data["username"]
    password = data["password"]
    password2 = data["password2"]
    # 동일 유저네임의 유저가 존재하는지 확인
    existing_user = db.users.find_one({"username": username})
    if existing_user:
        return jsonify({"ok": False, "err": "이미 존재하는 사용자입니다."})
    elif password != password2:
        return jsonify({"ok": False, "err": "비밀번호가 일치하지 않습니다."})
    else:
        # 동일 유저도 없고 암호도 서로 동일 시
        # 암호화한 비밀번호를 문서에 담아 db에 저장한다.
        password = password.encode("utf-8")
        hashed_password = hashpw(password, gensalt())
        doc = {"username": username, "password": hashed_password, "songs_liked": {}}
        db.users.insert_one(doc)
        return jsonify({"ok": True})

# 로그인 작업
@app.route("/login", methods=["GET", "POST"])
def login():
    # 로그인 된 유저 -> 돌려보낸다.
    if "username" in session:
        return redirect("/")
    if request.method == "POST":
        # 로그인 정보를 json으로 받는다.
        data = request.json
        username = data["username"]
        password = data["password"]
        # 유저네임으로 사용자를 찾는다.
        user = db.users.find_one({"username": username})
        if not user:
            # 사용자를 찾을 수 없습니다
            return jsonify({"msg": "사용자를 찾을 수 없습니다.", "redirect_url": "/login"})
        elif not checkpw(password.encode("utf-8"), user["password"]):
            # 비밀번호가 일치하지 않습니다
            return jsonify({"msg": "비밀번호가 일치하지 않습니다.", "redirect_url": "/login"})
        else:
            # 세션에 사용자명을 담고 랜딩?메인?으로 돌려보낸다
            session["username"] = username

            return jsonify({"msg": "성공!", "redirect_url": "/main"})
    else:
        return render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout():
    print(request.path)
    # 로그인되지 않은 사용자는 돌려보낸다
    if not session["username"]:
        return redirect("/")
    else:
        # 로그인 된 사용자는 세션을 지우고 돌려보낸다.
        session.clear()
        return redirect("/")


@app.route("/user/my-profile")
def profile():
    
     # 기본날씨 서울 종로구 기준 부여
    lat = env_variables["BASE_LAT"]
    lon = env_variables["BASE_LON"]
    # get_current_weather를 통해 날씨, 기온, 도시 이름을 받아옴
    current_weather, current_temp, current_city = "", "", ""
    if "current_weather" in session:
        # get-weather가 실행되면 session에 위의 세 정보가 실제 정보로 저장된다.
        current_weather = session["current_weather"]
        current_temp = session["current_temp"]
        current_city = session["current_city"]
    else:
        current_weather, current_temp, current_city = get_current_weather(lat, lon)
    # 로그인 되지 않은 사용자는 돌려보낸다.
    if not "username" in session:
        return redirect("/")
    else:
        # 로그인 된 사용자는 마이페이지로 이동한다 -> 작업 필요
        username = session["username"]
        user = db.users.find_one({"username": username}, {"_id": False})
        user_liked = user["songs_liked"]
        tracks = {
            "Sunny": [],
            "Cloudy": [],
            "Rainy": [],
            "Snowy": []
        }
        weathers = ["Sunny", "Cloudy", "Rainy", "Snowy"]
        for track in user_liked:
            for weather in weathers:
                if user_liked[track][weather] is True:
                    [title, artist, cover_image, preview_url] = get_track_info(track)
                    doc = {
                        "track_id": track,
                        "title": title,
                        "artist": artist,
                        "cover_image": cover_image,
                        "preview_url": preview_url
                    }
                    tracks[weather].append(doc)

        return render_template("mypage.html", username=session["username"], tracks=tracks, current_city=current_city, current_weather=current_weather, current_temp=current_temp)

@app.route("/get-weather", methods=["POST"])
def get_weather():
    # 기본 날씨 정보를 서울 종로구 좌표로 설정한다.
    lat = env_variables["BASE_LAT"]
    lon = env_variables["BASE_LON"]
    # post를 통해 좌표가 전해졌다면 바꾼다
    if request.json:
        position = request.json
        lat = position["lat"]
        lon = position["lon"]
    # 날씨, 기온, 도시를 받아온다.
    weather, weather_temp, weather_city = get_current_weather(lat, lon)
    # 세션에 현재 사용자의 날씨, 기온, 도시명을 담아 다른 곳에서도 활용할 수 있게 한다.
    session["current_weather"] = weather
    session["current_temp"] = weather_temp
    session["current_city"] = weather_city
    return jsonify({"weather": weather, "temp": weather_temp, "city": weather_city})

if __name__ == "__main__":
    app.run("0.0.0.0", env_variables["PORT"])


 