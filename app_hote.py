from cmath import pi
import code
from traceback import print_tb
from typing import Any
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint

import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding="utf-8")

# except 에서 http 에러를 핸들링 하기 위한 임포트
import urllib.request
from urllib.request import HTTPError

# -*- encoding: utf-8 -*-
"""
<함수 3개 정의>
1.트랙 id를 리스트로 리턴해주는 함수
2. 트랙 id를 인수로 받아 가수명, 곡명, 곡이미지, 곡 미리듣기를 리턴해주는 함수
3. 함수가 실행될 시 값이 이상하게 나오는 경우가 있어서 강제로 실행될 때까지 다시 작동하게 하는 함수
"""


# 1.트랙 id를 리스트로 리턴해주는 함수
def finding_trackId():

    cid = "e1e48c01f23740de885eff5fefba4db5"
    secret = "-"
    client_credentials_manager = SpotifyClientCredentials(
        client_id=cid, client_secret=secret
    )

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    cate_count = 50
    # 카테고리 50개를 가져옵니다.
    info_cate = sp.categories(country=None, locale=None, limit=cate_count, offset=0)

    # 실질 갯수가 함수 실행시 매번 변함. 따라서 실 개수를 알아야 for문을 돌릴 수 있다.
    count_sibal = len(info_cate["categories"]["items"])

    # 카테고리들의 아이디를 추출합니다.
    # 아이디를 담을 리스트도 위에 만들어줍니다.
    ids = []
    for i in range(count_sibal):
        try:
            id = info_cate["categories"]["items"][i]["id"]
            ids.append(id)
        except:
            continue

    # 카테 안의 플레이리스트의 아이디들을 추출
    # 플레이리스트 id를 담을 리스트 생성, 리스트 인덱스 파악
    play_id = []
    length = len(ids)

    for i in range(length):  # 최초 설정한 카테고리 갯수만큼 for문을 돌립니다.
        id_ = ids[i]  # 하나씩 빼오기
        # 오류를 생성하는 id가 있어서 오류 발생시에는 버리는 코드 작성
        try:
            list_id = sp.category_playlists(
                category_id=id_, country=None, limit=20, offset=0
            )
            real_total = len(list_id["playlists"]["items"])
            # id마다 가지고 있는 노래 개수가 달라서 인덱스 오류 방지를 위해 items 안의 컨텐츠 수를 받아서 for문을 돌림
            try:
                for i in range(real_total):
                    save = list_id["playlists"]["items"][i]["id"]
                    play_id.append(save)

            except:
                continue

        except:

            continue

    # 플레이리스트id를 통해 트랙 id 추출하기
    # 추출한 id를 담을 track_ids 리스트 만들기
    track_ids = []

    for i in play_id:
        try:
            # 각 플레이리스트 아이디마다 트랙 10개씩 뽑아오기
            # 존재하지 않는 id에 대비해 try 사용
            tracks = sp.playlist_items(
                i,
                fields=None,
                limit=3,
                offset=0,
                market=None,
                additional_types=("track", "episode"),
            )
            how_many = len(tracks["items"])
            try:
                for i in range(how_many):
                    c = tracks["items"][i]["track"]["id"]
                    track_ids.append(c)
            except:
                continue
        except:
            continue

    return track_ids


# 2. 트랙 id를 인수로 받아 가수명, 곡명, 곡이미지, 곡 미리듣기를 리턴해주는 함수
def giveout_etc(id):
    # 함수가 api의 내장함수를 기반으로 하는 함수로 api를 이용하기 위한 기본설정이 필수이다.
    cid = "e1e48c01f23740de885eff5fefba4db5"
    secret = "-"
    client_credentials_manager = SpotifyClientCredentials(
        client_id=cid, client_secret=secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    tracks_info = sp.track(id)

    # 가수이름, 곡명, 미리듣기, 이미지
    name = tracks_info["artists"][0]["name"]
    title = tracks_info["name"]
    preview = tracks_info["preview_url"]
    img = tracks_info["album"]["images"][0]["url"]

    # 리스트로 리턴해주기 사용할때 인덱스 사용하세요!
    answer = [name, title, preview, img]
    return answer


# 3. 함수가 실행될 시 값이 이상하게 나오는 경우가 있어서 강제로 실행될 때까지 다시 작동하게 하는 함수
def just_get_it_done():
    try:
        result = finding_trackId()
        return result
    except Exception as swear:
        just_get_it_done()


fucking_api = finding_trackId()


for i in fucking_api:
    try:
        print(giveout_etc(i))
    except:
        continue
