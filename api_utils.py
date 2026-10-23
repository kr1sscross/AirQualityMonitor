import requests
import os
from tkinter import messagebox
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"
AIR_QUALITY_URL = "http://api.openweathermap.org/data/2.5/air_pollution"


def calculate_aqi(pm2_5, pm10):
    try:
        return round(max(float(pm2_5), float(pm10)))
    except ValueError:
        messagebox.showerror("Error", "Invalid PM2.5 or PM10 data.")
        return None


def get_coordinates(city_name):
    try:
        params = {"q": city_name, "limit": 1, "appid": API_KEY}
        response = requests.get(GEO_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if data:
            return data[0]["lat"], data[0]["lon"], data[0]["name"]
        else:
            messagebox.showerror("Error", f"City not found: {city_name}")
            return None
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Connection problem: {e}")
        return None


def get_air_quality(lat, lon):
    try:
        params = {"lat": lat, "lon": lon, "appid": API_KEY}
        response = requests.get(AIR_QUALITY_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error fetching air quality data: {e}")
        return None