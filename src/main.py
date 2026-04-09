import threading
from config.settings import settings
from src.database.manager import DatabaseManager
from src.scheduler.jobs import GardenScheduler
import uvicorn


def main():
    platform = "Raspberry Pi" if settings.is_raspberry_pi else "Development machine"
    print(f"Smart Garden System starting on {platform}...")
    print(f"Database: {settings.database_path}")
    print(f"Sensor read interval: {settings.sensor_read_interval} min")

    db = DatabaseManager(settings.database_path)
    db.init_db()

    scheduler = GardenScheduler(db)
    scheduler.start()

    print("Scheduler running. Starting API server on port 8000...")
    try:
        uvicorn.run("src.api.app:app", host="0.0.0.0", port=8000, log_level="warning")
    except KeyboardInterrupt:
        scheduler.stop()
        print("Shutting down.")


if __name__ == "__main__":
    main()
