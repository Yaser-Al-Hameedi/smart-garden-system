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
        current_url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.latitude}&lon={self.longitude}&appid={self.api_key}&units=metric"
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={self.latitude}&lon={self.longitude}&appid={self.api_key}&units=metric&cnt=1"

        current = requests.get(current_url).json()
        forecast = requests.get(forecast_url).json()

        temperature = current["main"]["temp"]
        humidity = current["main"]["humidity"]
        description = current["weather"][0]["description"]
        rain_probability = forecast["list"][0]["pop"]

        self.db.save_weather_data(temperature, humidity, rain_probability, description)