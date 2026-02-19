from src.database.manager import DatabaseManager
from src.sensors.collector import SensorCollector


if __name__ == "__main__":

    db = DatabaseManager("data/test_garden.db")

    db.init_db()

    sensor_collector = SensorCollector(db)

    sensor_collector.collect()

    data = db.get_recent_sensor_readings()

    print(data)
