from src.sensors.base import BaseSensor
import time

try:
    import spidev
    import smbus2
    from w1thermsensor import W1ThermSensor
except ImportError:
    pass


class RealMoistureSensor(BaseSensor):
    def __init__(self, channel=0):
        self.channel = channel
        try:
            self.spi = spidev.SpiDev()
            self.spi.open(0, 0)
            self.spi.max_speed_hz = 1350000
        except Exception:
            self.spi = None

    def read(self):
        if self.spi is None:
            return 0.0
        adc = self.spi.xfer2([1, (8 + self.channel) << 4, 0])
        return ((adc[1] & 3) << 8) + adc[2]


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
        self.bus.write_byte(self.address, 0x20)
        time.sleep(0.2)
        data = self.bus.read_i2c_block_data(self.address, 0x00, 2)
        return (data[0] << 8 | data[1]) / 1.2
