from src.database.manager import DatabaseManager
from src.sensors.collector import SensorCollector
from src.pump.controller import PumpController
from src.models.predictor import Predictor


if __name__ == "__main__":

    db = DatabaseManager("data/test_garden.db")
    db.init_db()

    sensor_collector = SensorCollector(db)
    pump_collector = PumpController(db)

    sensor_collector.collect()

    reading = db.get_recent_sensor_readings(hours=1)[0]
    print("\n--- Sensor Reading ---")
    print(f"  Soil Moisture : {reading[1]:.1f} / 600 ({reading[1]/600*100:.1f}%)")
    print(f"  Temperature   : {reading[2]:.1f} C")
    print(f"  Light Level   : {reading[3]:.1f} lux")
    print(f"  Timestamp     : {reading[4]}")

    predictor = Predictor(db, pump_collector)
    predictor.predict_and_act()

    events = [e for e in db.get_recent_watering_events(hours=1) if e[4] >= reading[4]]
    print("\n--- Watering Decision ---")
    if events:
        e = events[0]
        print(f"  Decision      : Water")
        print(f"  Duration      : {e[1]:.1f} seconds")
        print(f"  Trigger       : {e[2]}")
        print(f"  Water Amount  : {e[3]:.1f} ml")
        print(f"  Timestamp     : {e[4]}")
    else:
        print("  Decision      : No watering needed")
