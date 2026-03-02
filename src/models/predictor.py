import os
import joblib
from config.settings import settings


class Predictor:
    def __init__(self, db, pump):
        self.db = db
        self.pump = pump
        self.model = None

        model_file = os.path.join(settings.model_path, "model.pkl")
        if os.path.exists(model_file):
            self.model = joblib.load(model_file)

    def predict_and_act(self):
        sensor_rows = self.db.get_recent_sensor_readings(hours=1)
        weather_rows = self.db.get_recent_weather_data(hours=1)

        if not sensor_rows:
            return

        latest_sensor = sensor_rows[0]
        soil_moisture = latest_sensor[1]

        rain_probability = 1.0
        if weather_rows:
            rain_probability = weather_rows[0][3]

        if self.model:
            features = [[soil_moisture, rain_probability]]
            should_water = bool(self.model.predict(features)[0])
            confidence = float(self.model.predict_proba(features)[0][1])
        else:
            should_water = soil_moisture < 400 and rain_probability < 0.3
            confidence = None

        if should_water:
            self.pump.water(
                duration_seconds=300,
                trigger="auto",
                model_confidence=confidence
            )
