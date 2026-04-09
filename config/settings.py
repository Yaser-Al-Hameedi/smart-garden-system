import platform
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # --- Platform ---
    is_raspberry_pi: bool = platform.system() == "Linux" and (platform.machine().startswith("arm") or platform.machine().startswith("aarch"))

    # --- Database ---
    database_path: str = str(BASE_DIR / "data" / "garden.db")

    # --- Sensor intervals (in minutes) ---
    sensor_read_interval: float = 0.5
    weather_fetch_interval: int = 60

    # --- Pump safety limits ---
    pump_max_duration: int = 10  # max minutes per watering
    pump_cooldown: int = 30  # min minutes between waterings

    # --- Weather API ---
    openweather_api_key: str = ""
    garden_latitude: float = 0.0
    garden_longitude: float = 0.0

    # --- ML Model ---
    model_path: str = str(BASE_DIR / "trained_models")
    plant_type: int = 1  # 0=Low, 1=Medium, 2=High water need
    pump_flow_rate: float = 52.0  # ml per second

    model_config = {
        "env_file": str(BASE_DIR / ".env"),
        "env_file_encoding": "utf-8",
        "protected_namespaces": ("settings_",),
    }


settings = Settings()
