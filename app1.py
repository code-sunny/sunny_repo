import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
 
cid = ''
secret = ''
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
# pprint.pprint()

# spotify안에 있는 카테고리들 출력해보기
info_cate = sp.categories(country=None, locale=None, limit=20, offset=0)
# pprint.pprint(info_cate)

# # 그중에 쩰루 인기있는 카테고리로 픽!
top_id = info_cate['categories']['items'][0]['id']


# # 첫번째는 카테의 정보인데 걍 쩌리, 두번째는 카테 안의 리스트
# cate_info = sp.category( top_id , country=None , locale=None )
cate_list = sp.category_playlists( category_id= top_id, country=None , limit=5 , offset=0 )
# pprint.pprint(cate_list)

# # id들을 담을 리스트 생성!
ids = []

# id들을 꺼내기 위한 준비, 리스트에 담긴 상태로 놓고, 인덱스 하나씩 열어서 꺼내버리기
dirty_ids = cate_list['playlists']['items']
# pprint.pprint(dirty_ids)
for i in dirty_ids:
    # print(i)
    # print('~'*100)

    single_id = i['id'] 
    ids.append(single_id)
    # print('~'*100)
    # print(single_id)
# pprint.pprint(first)
# print(ids)
final = []
for i in ids:
    tracks = sp.playlist_items(i, fields=None , limit=1 , offset=0 , market=None , additional_types=('track' , 'episode'))
    k = tracks['items'][0]['track']['artists'][0]['id']
    final.append(k)
    # print(k)
    # print('~'*100)

# print(final)
for i in final:
    name = sp.artist(i)
    real_name = name['name']
    real_id = name['id']
    print(real_name)
    print(real_id)
    # k = tracks['items'][0]
    # final.append(k)
    print('~'*100)

