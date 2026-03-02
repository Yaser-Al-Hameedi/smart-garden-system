import time
from config.settings import settings
from src.database.manager import DatabaseManager
from src.scheduler.jobs import GardenScheduler


def main():
    platform = "Raspberry Pi" if settings.is_raspberry_pi else "Development machine"
    print(f"Smart Garden System starting on {platform}...")
    print(f"Database: {settings.database_path}")
    print(f"Sensor read interval: {settings.sensor_read_interval} min")

    db = DatabaseManager(settings.database_path)
    db.init_db()

    scheduler = GardenScheduler(db)
    scheduler.start()

    print("Scheduler running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.stop()
        print("Shutting down.")


if __name__ == "__main__":
    main()
