from tkinter import Canvas, messagebox
from api_utils import calculate_aqi


def get_aqi_color_and_label(aqi):
    if aqi <= 50:
        return "#97E7B5", "Dobre"
    elif aqi <= 100:
        return "#F2DF7E", "Umiarkowane"
    elif aqi <= 150:
        return "#F2B67E", "Niezdrowe dla wrażliwych"
    elif aqi <= 200:
        return "#F28282", "Niezdrowe"
    else:
        return "#C190DC", "Bardzo niezdrowe"


def draw_rounded_card(canvas, x, y, w, h, r, color):
    shapes = [
        (canvas.create_oval, x - w // 2, y - h // 2, x - w // 2 + 2 * r, y - h // 2 + 2 * r),
        (canvas.create_oval, x + w // 2 - 2 * r, y - h // 2, x + w // 2, y - h // 2 + 2 * r),
        (canvas.create_oval, x - w // 2, y + h // 2 - 2 * r, x - w // 2 + 2 * r, y + h // 2),
        (canvas.create_oval, x + w // 2 - 2 * r, y + h // 2 - 2 * r, x + w // 2, y + h // 2),
        (canvas.create_rectangle, x - w // 2 + r, y - h // 2, x + w // 2 - r, y + h // 2),
        (canvas.create_rectangle, x - w // 2, y - h // 2 + r, x + w // 2, y + h // 2 - r)
    ]
    for func, x1, y1, x2, y2 in shapes:
        func(x1, y1, x2, y2, fill=color, outline="")


def display_data(result_frame, data, city_name):
    try:
        components = data["list"][0]["components"]
        pm2_5_value = components["pm2_5"]
        pm10_value = components["pm10"]

        aqi = calculate_aqi(pm2_5_value, pm10_value)
        if aqi is None:
            return

        card_color, air_status = get_aqi_color_and_label(aqi)

        for widget in result_frame.winfo_children():
            widget.destroy()

        card_width, card_height = 600, 280
        c = Canvas(result_frame, width=card_width, height=card_height, bg="#FAFAFA", highlightthickness=0)
        c.pack(pady=20)

        card_center_x = card_width // 2
        card_center_y = card_height // 2
        draw_rounded_card(c, card_center_x, card_center_y, card_width - 20, card_height - 20, 30, card_color)

        font_big = ("Helvetica", 22, "bold")
        font_medium = ("Helvetica", 16)
        font_small_bold = ("Helvetica", 14, "bold")

        # AQI i opis jakości powietrza
        c.create_text(card_center_x - 250, card_center_y - 80, text=f"{aqi} AQI+", font=font_big, fill="#333333", anchor="w")
        c.create_text(card_center_x - 250, card_center_y - 50, text=air_status, font=font_medium, fill="#333333", anchor="w")

        # Główny składnik zanieczyszczenia
        main_pollutant = "PM2.5" if pm2_5_value > pm10_value else "PM10"
        main_pollutant_value = max(pm2_5_value, pm10_value)
        c.create_text(card_center_x + 50, card_center_y - 80, text=f"Main pollutant:", font=font_small_bold, fill="#111111", anchor="w")
        c.create_text(card_center_x + 50, card_center_y - 50, text=f"{main_pollutant}: {main_pollutant_value:.2f} µg/m³", font=font_small_bold, fill="#111111", anchor="w")

        # PM2.5 i PM10 wartości
        c.create_text(card_center_x - 250, card_center_y + 10, text=f"PM2.5: {pm2_5_value:.2f} µg/m³", font=font_small_bold, fill="#111111", anchor="w")
        c.create_text(card_center_x + 50, card_center_y + 10, text=f"PM10: {pm10_value:.2f} µg/m³", font=font_small_bold, fill="#111111", anchor="w")
    except (KeyError, IndexError, TypeError) as e:
        messagebox.showerror("Błąd", f"Problem z przetwarzaniem danych: {e}")