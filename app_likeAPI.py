from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbplaylist

''' 메인페이지 좋아요 순위별 곡 (GET) 서버'''

@app.route('/main/song-rank', methods=['GET'])
def song_showRank():
    
    # 클라이언트에게 받은 이동 버튼 이름 저장
    weatherMoveBtn_receive = request.args['weatherMoveBtn_give']
    # 이동 버튼 정보를 바탕으로 순위별 데이터 10개 조회하여 저장
    song_rank = list(db.songs.find({}, {'_id' : False}).sort(weatherMoveBtn_receive, -1).limit(10))


    # 클라이언트 측으로 날씨, 순위별 곡 내려주기

    return jsonify ({'songs_rank' : song_rank})

''' 좋아요 API (GET) 서버 '''

@app.route('/api/show-like', methods=['GET'])
def song_showLike():
    
    # 클라이언트에게 받은 곡 이름 저장
    title_receive = request.args['title_give']
    
    # 클라이언트에게 받은 곡 가수 저장
    artist_receive = request.args['artist_give']
    

    # 클라이언트에게 받은 유저 닉네임 저장
    username_receive = request.args['username_give']

    # 클라이언트에게 받은 곡 정보를 조회하여 그 곡의 데이터 저장

    song = db.songs.find_one({"title" : title_receive, 'artist' : artist_receive}, {'_id' : False})
    
    # 클라이언트에게 받은 유저 닉네임, 버튼 정보를 조회하여 그 데이터 저장
    btn_like = db.users_songs.find_one({'username' : username_receive, "title" : title_receive, 'artist' : artist_receive}, {'_id' : False})   

    # 클라이언트 측으로 그 곡의 데이터를 보내주기
    return jsonify ({'target_song' : song, 'target_btn_like' : btn_like }) 


''' 좋아요 API (POST) 서버''' 

@app.route('/api/like-btn', methods=['POST'])
def like_btn():

    # 사용자가 버튼을 누른 곡 이름 : title_receive
    title_receive = request.form['title_give']
    print("-----------------")
    print(title_receive)
    print("-----------------")
    # 사용자가 버튼을 누른 곡 가수 : artist_receive
    artist_receive = request.form['artist_give']
    
    # 사용자가 어떤 버튼을 눌렀는지 정보 : weather_receive
    weatherBtn_receive = request.form['weatherBtn_give'] 

    # 사용자가 누른 버튼의 좋아요 상태 (현재 좋아요 눌린 상태인지 안 눌린 상태인지)
    is_weatherLike_receive = request.form['is_weatherLike_give']



    # 받아온 is_weatherLike_receive 가 true면 좋아요 -1 수행 / false면 좋아요 +1 수행
    ''' 좋아요 -1 기능'''
    # 좋아요 -1 기능은 이미 곡들이 DB에 있는 상태!
    # 따라서, db를 조회해서 사용자가 누른 곡과 날씨 버튼에 맞는 데이터를 찾아서 좋아요 -1
    if is_weatherLike_receive == "true":

        song = db.songs.find_one({'title':title_receive, 'artist' : artist_receive})
        
        minus_like = song[weatherBtn_receive] -1 
        db.songs.update_one({'title' : title_receive, 'artist' : artist_receive}, {'$set' : {weatherBtn_receive : minus_like}})
        
    
    else:
        ''' 좋아요 +1 기능 '''
            
        # 사용자가 누른 곡의 정보 조회해서 song, artist에 저장
        # 이때, 곡 이름 변수 저장 시 곡 이름이 같고 아티스트가 다른 데이터 있을 수 있으므로 이름과 아티스트 둘 다 체크
        # 이때, 곡 가수 변수 저장 시 아티스트가 같고 곡 이름이 다른 데이터 있을 수 있으므로 이름과 아티스트 둘 다 체크
        song = db.songs.find_one({'title':title_receive, 'artist' : artist_receive})


        # db에 없다면 추가할 default 데이터
        songs_doc = {'title' : title_receive, 
            'artist' : artist_receive, 
            'Sunny' : 0, 
            'Cloudy' : 0, 
            'Rainy' : 0, 
            'Snowy' : 0,
            }

        # if) 사용자가 누른 곡 이름이 db에 없다면, db에 default 값으로 추가 후
        # 사용자가 누른 버튼에 맞게 좋아요 수 +1
        if song == None:        
            db.songs.insert_one(songs_doc)
            song = db.songs.find_one({'title':title_receive, 'artist' : artist_receive})
            plus_like = song[weatherBtn_receive] +1 
            db.songs.update_one({'title' : title_receive, 'artist' : artist_receive}, {'$set' : {weatherBtn_receive : plus_like}})

        # else) 이미 db에 곡 정보가 있다면 조회해서 좋아요 수 +1
        else:
            plus_like = song[weatherBtn_receive] +1 
            db.songs.update_one({'title' : title_receive, 'artist' : artist_receive}, {'$set' : {weatherBtn_receive : plus_like}})       
        
        ''' 좋아요 눌렀을 때 로그인 여부 판단 '''       
            
        # 사용자의 닉네임 정보 : username_receive
        username_receive = request.form['username_give']     

        # 사용자의 닉네임 정보를 찾아서 변수에 저장
        username = db.users.find_one({'username' : username_receive})

        if username == None:
            return jsonify({'msg' : "로그인을 해주세요!", 'redirect_url' : "/login"})
        
        
    ''' 좋아요 누르거나 취소했을 때 날씨_like True / False로 업데이트 '''



    # username이 있을 때, Sunny_like 필드가 있는지 없는지 체크 (없으면 None 반환 -> 가입 후 처음 버튼 누르는 사람)
   
    # 사용자의 닉네임 정보 : username_receive
    username_receive = request.form['username_give'] 
    
    users_songs = db.users_songs.find_one({'username' : username_receive, 'title' : title_receive, 'artist' : artist_receive} )

    # users_songs db 초기화
    users_songs_doc = {'username' : username_receive, 'title' : title_receive, 'artist' : artist_receive, 'Sunny' : False, 'Cloudy' : False, 'Rainy' : False, 'Snowy' : False,}
    
    # 사용자가 처음 곡에 좋아요를 눌렀을 때
    if users_songs == None:
        db.users_songs.insert_one(users_songs_doc)     
        db.users_songs.update_one({'username' : username_receive}, {'$set' : {weatherBtn_receive : True}})


    # 사용자가 곡에 좋아요를 처음 누른 게 아닐때
    else:
        # 사용자가 좋아요를 눌렀을 때 (현재 버튼이 좋아요를 누른 상태가 아닐 때)
        if users_songs[weatherBtn_receive] == False:

            db.users_songs.update_one({'username' : username_receive, 'title' : title_receive, 'artist' : artist_receive}, {'$set' : {weatherBtn_receive : True}})
        
        # 사용자가 좋아요를 취소했을 때 (현재 버튼이 좋아요를 누른 상태일 때)
        else:
            db.users_songs.update_one({'username' : username_receive, 'title' : title_receive, 'artist' : artist_receive}, {'$set' : {weatherBtn_receive : False}})
        
    return jsonify({'msg' : "날씨 버튼 좋아요 +1 완료!"})




''' 로그인 페이지 이동 API '''

@app.route("/login")
def login_home():
    return render_template("login.html")


''' 서버 구동 API '''

@app.route('/')
def home():
    return render_template("sunny.html")



if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)