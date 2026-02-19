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
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

    def read(self):
        value = GPIO.input(self.pin)
        return value * 1023


class RealTemperatureSensor(BaseSensor):
    def __init__(self):
        self.w1 = W1ThermSensor()

    def read(self):
        return self.w1.get_temperature()


class RealLightSensor(BaseSensor):
    def __init__(self, address=0x23):
        self.bus = smbus2.SMBus(1)
        self.address = address

    def read(self):
        data = self.bus.read_i2c_block_data(self.address, 0x20, 2)
        return (data[0] * 256 + data[1]) / 1.2
        

