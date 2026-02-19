from src.sensors.base import BaseSensor
import random

class MockSoilMoistureSensor(BaseSensor):
    def __init__(self):
        pass

    def read(self):
        return random.uniform(300, 800)

class MockTemperatureSensor(BaseSensor):
    def __init__(self):
        pass

    def read(self):
        return random.uniform(15.0, 35.0)

class MockLightSensor(BaseSensor):
    def __init__(self):
        pass

    def read(self):
        return random.uniform(100, 1000)
