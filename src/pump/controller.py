from config.settings import settings
import time
from datetime import datetime

try:
    import RPi.GPIO as GPIO
except ImportError:
    pass

class PumpController:
    def __init__(self, db):
        self.db = db
        self.relay_pin = 17
        self.last_watered = None
        if settings.is_raspberry_pi:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.relay_pin, GPIO.OUT)
    
    def water(self, duration_seconds, trigger, model_confidence=None):
        if self.last_watered is not None:
            seconds_since_last = (datetime.now() - self.last_watered).total_seconds()
            if seconds_since_last < settings.pump_cooldown * 60:
                return

        duration_seconds = min(duration_seconds, settings.pump_max_duration * 60)

        if settings.is_raspberry_pi:
            GPIO.output(self.relay_pin, GPIO.HIGH)
            time.sleep(duration_seconds)
            GPIO.output(self.relay_pin, GPIO.LOW)
        else:
            print(f"[MOCK] Pump ON for {duration_seconds} seconds")
            time.sleep(duration_seconds)
            print("[MOCK] Pump OFF")

        self.last_watered = datetime.now()
        self.db.save_watering_event(duration_seconds, trigger, model_confidence)




