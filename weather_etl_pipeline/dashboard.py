import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime, date
import time

# -------------------------------
# Configuration
# -------------------------------
DB_PATH = "weather.db"
REFRESH_INTERVAL = 10  # seconds

st.set_page_config(page_title="🌤️ Real-Time Weather Dashboard", layout="wide")

# -------------------------------
# Database Helper
# -------------------------------
def load_data_from_db():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM weather", conn)
    conn.close()
    return df

# -------------------------------
# Preprocess Data
# -------------------------------
def preprocess_data(df):
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date
    df["temp_celsius"] = df["temperature"]
    return df

def get_today_data(df):
    today = date.today()
    return df[df["date"] == today]

def get_latest_data(df):
    return df.sort_values("timestamp").drop_duplicates("city", keep="last")

# -------------------------------
# Charts
# -------------------------------
def plot_temperature_comparison(df):
    fig = px.line(
        df,
        x="timestamp",
        y=["temp_celsius", "feels_like"],
        title="🌡️ Temperature vs Feels Like (Today)"
    )
    fig.update_layout(xaxis_title="Time", yaxis_title="Temperature (°C)")
    st.plotly_chart(fig, use_container_width=True)

def plot_humidity_trends(df):
    fig = px.line(
        df,
        x="timestamp",
        y="humidity",
        title="💧 Humidity Trends (Today)"
    )
    fig.update_layout(xaxis_title="Time", yaxis_title="Humidity (%)")
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# Streamlit App
# -------------------------------
def main():
    st.title("🌤️ Real-Time Weather Dashboard")
    st.subheader(f"Auto-updates every {REFRESH_INTERVAL} seconds")

    df = load_data_from_db()
    if df.empty:
        st.warning("⚠️ No data available yet...")
    else:
        df = preprocess_data(df)
        today_df = get_today_data(df)

        if today_df.empty:
            st.warning("⚠️ No data for today yet...")
        else:
            latest_data = get_latest_data(today_df)

            # Charts
            col1, col2 = st.columns(2)
            with col1:
                plot_temperature_comparison(today_df)
            with col2:
                plot_humidity_trends(today_df)

            # Latest table
            st.subheader("📌 Latest Weather Data (Today)")
            st.dataframe(latest_data, use_container_width=True)

    # 🔄 Auto-refresh with rerun
    time.sleep(REFRESH_INTERVAL)
    st.rerun()



# -------------------------------
if __name__ == "__main__":
    main()
