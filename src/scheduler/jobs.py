from apscheduler.schedulers.background import BackgroundScheduler
from src.sensors.collector import SensorCollector
from src.weather.client import WeatherClient
from src.pump.controller import PumpController
from src.models.predictor import Predictor
from config.settings import settings

class GardenScheduler:
    def __init__(self, db):
        self.db = db
        self.collector = SensorCollector(db)
        self.weather = WeatherClient(db)
        self.pump = PumpController(db)
        self.predictor = Predictor(db, self.pump)
        self.scheduler = BackgroundScheduler()

    def start(self):
        self.scheduler.add_job(self.collector.collect, 'interval', minutes=settings.sensor_read_interval)
        self.scheduler.add_job(self.weather.fetch_and_save, 'interval', minutes=settings.weather_fetch_interval)
        self.scheduler.add_job(self.predictor.predict_and_act, 'interval', minutes=settings.sensor_read_interval)
        self.scheduler.start()

    def stop(self):
        self.scheduler.shutdown()