from spotify import sp

def get_track_ids():
    category_count = 20
    
    category_infos = sp.categories(country="KR", locale="KR", limit=category_count, offset=5)["categories"]["items"]
    # categories = len(category_infos["categories"]["items"])

    category_ids = []
    for category in category_infos:
        id = category["id"]
        category_ids.append(id)

    playlist_ids = []
    for _id in category_ids:
        lists = sp.category_playlists(
            category_id=_id, country="KR", limit=5, offset=1 
        )["playlists"]["items"]
        for playlist in lists:
            playlist_id = playlist["id"]
            playlist_ids.append(playlist_id)
    
    track_ids = []
    for playlist_id in playlist_ids:
        tracks = sp.playlist_items(
            playlist_id=playlist_id,
            limit=2,
            fields="items,track",
            market=None,
        )["items"]
        for track in tracks:
            track_id = track["track"]["id"]
            track_ids.append(track_id)

    return track_ids

def new_song(track_id, title, artist, preview_url, cover_image):
    doc = {
        "track_id": track_id,
        "title": title,
        "artist": artist,
        "preview_url": preview_url,
        "cover_image": cover_image,
        "likes": {"Sunny": 0, "Rainy": 0, "Cloudy": 0, "Snowy": 0},
        "likedUsers": []
    }
    return doc


    