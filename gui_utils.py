import customtkinter as ctk
from CTkMessagebox import CTkMessagebox


def aqi_colors(aqi: int) -> tuple[str, str]:
    match aqi:
        case 1:
            return "#97E7B5", "Good"
        case 2:
            return "#F2DF7E", "Fair"
        case 3:
            return "#F2B67E", "Moderate"
        case 4:
            return "#F28282", "Poor"
        case 5:
            return "#C190DC", "Very Poor"
        case _:
            return "white", "Unknown"

def display_data(result_frame: ctk.CTkFrame, data: dict, city_name: str) -> None:
    try:
        air_data = data["list"][0]
        components = air_data["components"]

        aqi = air_data["main"]["aqi"]
        pm2_5_value = float(components["pm2_5"])
        pm10_value = float(components["pm10"])

        if pm2_5_value < 0 or pm10_value < 0:
            raise ValueError("PM values cannot be negative.")

        card_color, air_status = aqi_colors(aqi)

        for widget in result_frame.winfo_children():
            widget.destroy()

        card = ctk.CTkFrame(result_frame, width=500, height=250, corner_radius=25, fg_color=card_color)
        card.pack(padx=20, pady=20)
        card.pack_propagate(False)

        city_label = ctk.CTkLabel(card, text=city_name, font=("Arial", 22, "bold"), text_color="#333333")
        city_label.pack(pady=(15, 0))

        aqi_label = ctk.CTkLabel(card, text=f"AQI: {aqi}", font=("Arial", 32, "bold"), text_color="#333333")
        aqi_label.pack(pady=(5, 0))

        status_label = ctk.CTkLabel(card, text=air_status, font=("Arial", 18), text_color="#333333")
        status_label.pack(pady=(0, 15))

        pm_frame = ctk.CTkFrame(card, fg_color="transparent")
        pm_frame.pack(fill="x", padx=20, pady=5)

        pm25_label = ctk.CTkLabel(pm_frame, text=f"PM2.5\n{pm2_5_value:.2f} µg/m³", font=("Arial", 15, "bold"), text_color="#333333")
        pm25_label.grid(row=0, column=0, padx=20, pady=5)

        pm10_label = ctk.CTkLabel(pm_frame, text=f"PM10\n{pm10_value:.2f} µg/m³", font=("Arial", 15, "bold"), text_color="#333333")
        pm10_label.grid(row=0, column=1, padx=20, pady=5)

        pm_frame.grid_columnconfigure((0, 1), weight=1)

    except (KeyError, IndexError, TypeError, ValueError) as e:
        CTkMessagebox(title="Error", message=f"Unable to process air quality data: {e}", icon="cancel")