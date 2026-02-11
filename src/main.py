from config.settings import settings


def main():
    platform = "Raspberry Pi" if settings.is_raspberry_pi else "Development machine"
    print(f"Smart Garden System starting on {platform}...")
    print(f"Database: {settings.database_path}")
    print(f"Sensor read interval: {settings.sensor_read_interval} min")


if __name__ == "__main__":
    main()
