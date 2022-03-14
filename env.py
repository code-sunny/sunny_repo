import os

env_variables = {
    "PORT": os.getenv("PORT"),
    "BASE_LAT": os.getenv("BASE_LAT"),
    "BASE_LON": os.getenv("BASE_LON"),
    "OPENWEATHER_KEY": os.getenv("SERVICE_KEY"),
    "SPOTIFY_ID": os.getenv("SPOTIFY_CLIENT_ID"),
    "SPOTIFY_SECRET": os.getenv("SPOTIFY_CLIENT_SECRET"),
    "FLASK_SECRET": os.getenv("APP_SECRET"),
    "YOUTUBE_KEY": os.getenv("YOUTUBE_KEY")
}
