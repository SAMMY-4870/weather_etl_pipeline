import sqlite3
import requests
from datetime import datetime

# -------------------------------
# Config
# -------------------------------
DB_PATH = "weather.db"
API_KEY = "bff9cdee2747a19a6077c450cf394738"   # 🔑 replace with your key
CITIES = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Pune", "Nagpur", "Hyderabad"]

# -------------------------------
# Create table if not exists
# -------------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
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

# -------------------------------
# Fetch weather from OpenWeather
# -------------------------------
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

# -------------------------------
# Insert into SQLite
# -------------------------------
def insert_weather(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO weather (city, temperature, feels_like, humidity, wind_speed, description, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (data["city"], data["temperature"], data["feels_like"], data["humidity"], 
          data["wind_speed"], data["description"], data["timestamp"]))
    conn.commit()
    conn.close()

# -------------------------------
# Main Job
# -------------------------------
def main():
    init_db()
    for city in CITIES:
        try:
            weather = fetch_weather(city)
            insert_weather(weather)
            print(f"✅ Data inserted for {city} at {weather['timestamp']}")
        except Exception as e:
            print(f"❌ Error fetching data for {city}: {e}")

if __name__ == "__main__":
    main()
