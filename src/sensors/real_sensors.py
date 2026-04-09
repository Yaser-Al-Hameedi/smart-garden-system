from src.sensors.base import BaseSensor
import time
import glob

try:
    import spidev
    import smbus2
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
        matches = glob.glob('/sys/bus/w1/devices/28-*/w1_slave')
        self.device_file = matches[0] if matches else None

    def read(self):
        if self.device_file is None:
            return 0.0
        try:
            with open(self.device_file, 'r') as f:
                lines = f.readlines()
            if lines[0].strip()[-3:] != 'YES':
                return 0.0
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                return float(lines[1][equals_pos + 2:]) / 1000.0
        except Exception:
            return 0.0
        return 0.0


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
        self.bus.write_byte(self.address, 0x10)
        time.sleep(0.2)
        data = self.bus.read_i2c_block_data(self.address, 0x00, 2)
        return (data[0] << 8 | data[1]) / 1.2
