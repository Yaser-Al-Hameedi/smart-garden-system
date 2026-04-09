from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.database.manager import DatabaseManager
from src.pump.controller import PumpController
from config.settings import settings
from pathlib import Path

STATIC_DIR = Path(__file__).resolve().parent.parent.parent / "static"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

db = DatabaseManager(settings.database_path)
db.init_db()
pump = PumpController(db)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/sensors/current")
def get_current_sensor():
    rows = db.get_recent_sensor_readings(hours=1)
    if not rows:
        return {}
    row = rows[0]
    return {"id": row[0], "soil_moisture": row[1], "temperature": row[2], "light_level": row[3], "timestamp": row[4]}


@app.get("/api/sensors/history")
def get_sensor_history(hours: int = 24):
    rows = db.get_recent_sensor_readings(hours=hours)
    return [{"id": r[0], "soil_moisture": r[1], "temperature": r[2], "light_level": r[3], "timestamp": r[4]} for r in rows]


@app.get("/api/weather/current")
def get_current_weather():
    rows = db.get_recent_weather_data(hours=1)
    if not rows:
        return {}
    row = rows[0]
    return {"id": row[0], "temperature": row[1], "humidity": row[2], "rain_probability": row[3], "description": row[4], "timestamp": row[5]}


@app.get("/api/watering/history")
def get_watering_history(hours: int = 24):
    rows = db.get_recent_watering_events(hours=hours)
    return [{"id": r[0], "duration_seconds": r[1], "trigger": r[2], "model_confidence": r[3], "timestamp": r[4]} for r in rows]


@app.post("/api/watering/manual")
def manual_water(duration_seconds: int = 300):
    pump.water(duration_seconds=duration_seconds, trigger="manual")
    return {"status": "ok", "duration_seconds": duration_seconds}


@app.get("/api/system/status")
def get_system_status():
    platform = "Raspberry Pi" if settings.is_raspberry_pi else "Development machine"
    recent_readings = db.get_recent_sensor_readings(hours=1)
    last_reading = recent_readings[0][4] if recent_readings else None
    return {
        "platform": platform,
        "sensor_read_interval_min": settings.sensor_read_interval,
        "weather_fetch_interval_min": settings.weather_fetch_interval,
        "last_sensor_reading": last_reading,
    }
