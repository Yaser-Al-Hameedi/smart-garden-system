from config.settings import settings
import requests
from src.database.manager import DatabaseManager


class WeatherClient():

    def __init__(self, db):
        self.db = db
        self.latitude = settings.garden_latitude
        self.longitude = settings.garden_longitude
        self.api_key = settings.openweather_api_key
    
    def fetch_and_save(self):
        
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.latitude}&lon={self.longitude}&appid={self.api_key}&units=metric"
        response = requests.get(url)
        json_dict = response.json()

        temperature = json_dict["main"]["temp"]
        humidity = json_dict["main"]["humidity"]
        rain_probability = json_dict.get("rain", {}).get("1h", 0.0) / 100
        description = json_dict["weather"][0]["description"]

        self.db.save_weather_data(temperature, humidity, rain_probability, description)