import requests
from tkinter import messagebox

API_KEY = "b7d1dfa2aa89a9c6d240f11a6a8e3843"
GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"
AIR_QUALITY_URL = "http://api.openweathermap.org/data/2.5/air_pollution"


def calculate_aqi(pm2_5, pm10):
    try:
        return round(max(float(pm2_5), float(pm10)))
    except ValueError:
        messagebox.showerror("Błąd", "Nieprawidłowe dane PM2.5 lub PM10.")
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
            messagebox.showerror("Błąd", f"Nie znaleziono miasta: {city_name}")
            return None
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Błąd", f"Problem z połączeniem: {e}")
        return None


def get_air_quality(lat, lon):
    try:
        params = {"lat": lat, "lon": lon, "appid": API_KEY}
        response = requests.get(AIR_QUALITY_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Błąd", f"Problem z pobraniem danych jakości powietrza: {e}")
        return None