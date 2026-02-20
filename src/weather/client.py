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
        
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={self.latitude}&lon={self.longitude}&appid={self.api_key}&units=metric"
        response = requests.get(url)
        json_dict = response.json()

        temperature = json_dict["current"]["temp"]
        humidity = json_dict["current"]["humidity"]
        rain_probability = json_dict["hourly"][0]["pop"]
        description = json_dict["current"]["weather"][0]["description"]

        self.db.save_weather_data(temperature, humidity, rain_probability, description)