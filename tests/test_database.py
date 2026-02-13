from src.database.manager import DatabaseManager

if __name__ == "__main__":

    db = DatabaseManager("data/test_garden.db")

    db.init_db()

    db.save_sensor_reading(450.0, 22.5, 800.0)

    data = db.get_recent_sensor_readings()

    print(data)

