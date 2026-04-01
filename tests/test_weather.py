from src.database.manager import DatabaseManager
from src.weather.client import WeatherClient

if __name__ == "__main__":
    db = DatabaseManager("data/test_garden.db")
    db.init_db()

    client = WeatherClient(db)
    client.fetch_and_save()

    data = db.get_recent_weather_data(hours=1)
    print("Weather data saved:", data[0])
