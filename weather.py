import requests
from env import env_variables

def get_current_weather(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "units": "metric",
        "appid": env_variables["OPENWEATHER_KEY"]
    }
    response = requests.get(url, params=params)
    json = response.json()
    weather_id = json["weather"][0]["id"]
    weather_temp = json["main"]["temp"]
    weather_city = json["name"]
    weather = ""
    if weather_id == 800:
        weather = "Sunny"
    elif weather_id >= 200 and weather_id < 600:
        weather = "Rainy"
    elif weather_id >= 600 and weather_id < 700:
        weather = "Snowy"
    elif weather_id >= 700 and weather_id < 805:
        weather = "Cloudy"
    return [weather, weather_temp, weather_city]