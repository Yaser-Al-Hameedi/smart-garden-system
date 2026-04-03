from src.sensors.base import BaseSensor

try:
    import RPi.GPIO as GPIO
    from w1thermsensor import W1ThermSensor
    import smbus2
except ImportError:
    pass


class RealMoistureSensor(BaseSensor):
    def __init__(self, pin):
        self.pin = pin
        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.IN)
        except Exception:
            self.pin = None

    def read(self):
        if self.pin is None:
            return 0.0
        return GPIO.input(self.pin) * 1023


class RealTemperatureSensor(BaseSensor):
    def __init__(self):
        try:
            self.w1 = W1ThermSensor()
        except Exception:
            self.w1 = None

    def read(self):
        if self.w1 is None:
            return 0.0
        return self.w1.get_temperature()


class RealLightSensor(BaseSensor):
    def __init__(self, address=0x23):
        try:
            self.bus = smbus2.SMBus(1)
            self.address = address
        except Exception:
            self.bus = None

    def read(self):
        if self.bus is None:
            return 0.0
        data = self.bus.read_i2c_block_data(self.address, 0x20, 2)
        return (data[0] * 256 + data[1]) / 1.2
        

