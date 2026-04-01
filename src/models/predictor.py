import os
import joblib
import pandas as pd
from config.settings import settings


class Predictor:
    def __init__(self, db, pump):
        self.db = db
        self.pump = pump
        self.model = None

        model_file = os.path.join(settings.model_path, "water_amount_regression_model.pkl")
        if os.path.exists(model_file):
            self.model = joblib.load(model_file)

    def predict_and_act(self):
        sensor_rows = self.db.get_recent_sensor_readings(hours=1)
        weather_rows = self.db.get_recent_weather_data(hours=1)

        if not sensor_rows:
            return

        latest_sensor = sensor_rows[0]
        soil_moisture_raw = latest_sensor[1]
        temperature = latest_sensor[2]
        light_lux = latest_sensor[3]

        rain_probability = 0.0
        if weather_rows:
            rain_probability = weather_rows[0][3]

        # Convert to units the model expects
        soil_moisture_percent = (soil_moisture_raw / 600) * 100
        rain_probability_percent = rain_probability * 100

        if self.model:
            features = pd.DataFrame([{
                "SoilMoisture_Percent": soil_moisture_percent,
                "Light_Lux": light_lux,
                "Temperature_C": temperature,
                "Rain_Probability_Percent": rain_probability_percent,
                "Plant_Type": settings.plant_type
            }])
            water_ml = float(self.model.predict(features)[0])
        else:
            # Rule-based fallback
            should_water = soil_moisture_percent < 40 and rain_probability < 0.3
            water_ml = 500 if should_water else 0

        if water_ml > 0:
            duration_seconds = water_ml / settings.pump_flow_rate
            self.pump.water(
                duration_seconds=duration_seconds,
                trigger="auto",
                model_confidence=water_ml
            )
