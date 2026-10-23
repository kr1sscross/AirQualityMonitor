import os
import requests
from CTkMessagebox import CTkMessagebox
from dotenv import load_dotenv


load_dotenv()

def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise ValueError(f"{name} must be set in .env")

    return value

API_KEY = get_required_env("API_KEY")
GEO_URL = get_required_env("GEO_URL")
AIR_QUALITY_URL = get_required_env("AIR_QUALITY_URL")

def coordinates(city: str) -> tuple[float, float, str] | None:
    try:
        params = {"q": city, "limit": 1, "appid": API_KEY}
        response = requests.get(GEO_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data:
            return data[0]["lat"], data[0]["lon"], data[0]["name"]
        else:
            CTkMessagebox(title="Error", message=f"City not found!", icon="cancel")
            return None
    except requests.exceptions.RequestException as e:
        CTkMessagebox(title="Error", message=f"Connection problem: {e}", icon="cancel")
        return None

def air_quality_data(lat: float, lon: float) -> dict | None:
    try:
        params = {"lat": lat, "lon": lon, "appid": API_KEY}
        response = requests.get(AIR_QUALITY_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        CTkMessagebox(title="Error", message=f"Error fetching air quality data: {e}", icon="cancel")
        return None

def aqi_data(data: dict) -> int | None:
    try:
        return data["list"][0]["main"]["aqi"]
    except (KeyError, IndexError, TypeError):
        return None
