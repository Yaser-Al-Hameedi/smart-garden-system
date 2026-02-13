import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
    
    def connect(self):
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        connection = self.connect()
        cursor = connection.cursor()

        '''
        For our Pi's physical sensors
        '''
        cursor.execute("""CREATE TABLE IF NOT EXISTS sensor_readings ( 
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        soil_moisture REAL NOT NULL,
                        temperature REAL NOT NULL,
                        light_level REAL NOT NULL,
                        timestamp TEXT NOT NULL)""")
        '''
        This table will hold infomration retrieved from our weather API
        '''
        cursor.execute("""CREATE TABLE IF NOT EXISTS weather_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        temperature REAL NOT NULL,
                        humidity REAL NOT NULL,
                        rain_probability REAL NOT NULL,
                        description TEXT NOT NULL,
                        timestamp TEXT NOT NULL
                                                )""")
        '''
        This table will log every time the water pump gets used
        '''
        cursor.execute("""CREATE TABLE IF NOT EXISTS watering_events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        duration_seconds INTEGER NOT NULL,
                        trigger TEXT NOT NULL,
                        model_confidence REAL,
                        timestamp TEXT NOT NULL
                                                )""")
        '''
        This table is for debugging and montoring
        '''
        cursor.execute("""CREATE TABLE IF NOT EXISTS system_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        level TEXT NOT NULL,
                        message TEXT NOT NULL,
                        timestamp TEXT NOT NULL
                                                )""")
        connection.commit()
        connection.close()


    # Methods to add respective data into tables
    def save_sensor_reading(self, soil_moisture, temperature, light_level):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("INSERT INTO sensor_readings (soil_moisture, temperature, light_level, timestamp) VALUES (?, ?, ?, ?)",
                       (soil_moisture, temperature, light_level, datetime.now().isoformat()))
        
        connection.commit()
        connection.close()
    

    
    def save_weather_data(self, temperature, humidity, rain_probability, description):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("INSERT into weather_data (temperature, humidity, rain_probability, description, timestamp) VALUES (?, ?, ?, ?, ?)", 
                       (temperature, humidity, rain_probability, description, datetime.now().isoformat()))

        connection.commit()
        connection.close()


    def save_watering_event(self, duration_seconds, trigger, model_confidence):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("INSERT into watering_events (duration_seconds, trigger, model_confidence, timestamp) VALUES (?, ?, ?, ?)", 
                       (duration_seconds, trigger, model_confidence, datetime.now().isoformat()))
    
        connection.commit()
        connection.close()


    def save_system_log(self, level, message):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("INSERT into system_logs (level, message, timestamp) VALUES (?, ?, ?)", 
                       (level, message, datetime.now().isoformat()))
        
        connection.commit()
        connection.close()
    


    # Query Methods for dashboard and ML model to read data
    def get_recent_sensor_readings(self, hours=24):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM sensor_readings WHERE timestamp >= ? ORDER BY timestamp DESC", 
                       ((datetime.now() - timedelta(hours=hours)).isoformat(),))
        
        rows = cursor.fetchall()
        connection.close()
        return rows
    
    
    def get_recent_weather_data(self, hours=24):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM weather_data WHERE timestamp >= ? ORDER BY timestamp DESC", 
                       ((datetime.now() - timedelta(hours=hours)).isoformat(),))
        
        rows = cursor.fetchall()
        connection.close()
        return rows

    
    def get_recent_watering_events(self, hours=24):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM watering_events WHERE timestamp >= ? ORDER BY timestamp DESC", 
                       ((datetime.now() - timedelta(hours=hours)).isoformat(),))
        
        rows = cursor.fetchall()
        connection.close()
        return rows
    

    def get_recent_system_logs(self, hours=24):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM system_logs WHERE timestamp >= ? ORDER BY timestamp DESC", 
                       ((datetime.now() - timedelta(hours=hours)).isoformat(),))
        
        rows = cursor.fetchall()
        connection.close()
        return rows


