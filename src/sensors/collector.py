from src.database.manager import DatabaseManager
from config.settings import settings
from src.sensors.mock_sensors import MockLightSensor, MockSoilMoistureSensor, MockTemperatureSensor
from src.sensors.real_sensors import RealLightSensor, RealMoistureSensor, RealTemperatureSensor


class SensorCollector():

    def __init__(self, db):
        self.db = db

        if settings.is_raspberry_pi:
            self.moisture = RealMoistureSensor(pin=17)
            self.temperature = RealTemperatureSensor()
            self.light = RealLightSensor()
        else:
            self.moisture = MockSoilMoistureSensor()
            self.temperature = MockTemperatureSensor()
            self.light = MockLightSensor()
    
    def collect(self):
        moisture = self.moisture.read()
        temp = self.temperature.read()
        light = self.light.read()

        self.db.save_sensor_reading(moisture, temp, light)
        