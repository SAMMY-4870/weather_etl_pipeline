import requests
import pandas as pd
import sqlite3
import time
from datetime import datetime

# Config
API_KEY = "bff9cdee2747a19a6077c450cf394738"   # replace with your OpenWeather API key
CITIES = ["Delhi", "Mumbai", "Pune", "Nagpur", "Bangalore", "Chennai", "Kolkata", "Hyderabad"]
DB_PATH = "weather.db"
CSV_PATH = "data/weather_data.csv"

# Initialize DB only once
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            city TEXT,
            temperature REAL,
            feels_like REAL,
            humidity INTEGER,
            wind_speed REAL,
            description TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

# Fetch weather data
def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    return {
        "city": city,
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "description": data["weather"][0]["description"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# Insert rows manually into SQLite
def insert_to_db(data):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO weather (city, temperature, feels_like, humidity, wind_speed, description, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["city"], data["temperature"], data["feels_like"],
        data["humidity"], data["wind_speed"], data["description"],
        data["timestamp"]
    ))
    conn.commit()
    conn.close()

# Main ETL
def main():
    init_db()
    
    all_data = []
    for city in CITIES:
        weather = fetch_weather(city)
        all_data.append(weather)
        insert_to_db(weather)   # ✅ insert row directly into DB
        print(f"Stored: {city} → {weather['temperature']}°C (feels {weather['feels_like']}°C), "
              f"{weather['humidity']}%, {weather['wind_speed']} m/s, {weather['description']}")
    
    # Convert to DataFrame
    df = pd.DataFrame(all_data)
    
    # Save to CSV (append if exists)
    try:
        old_df = pd.read_csv(CSV_PATH)
        df = pd.concat([old_df, df], ignore_index=True)
    except FileNotFoundError:
        pass
    
    df.to_csv(CSV_PATH, index=False)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(30)  # fetch every 30 sec
