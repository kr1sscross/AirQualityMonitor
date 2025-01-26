import tkinter as tk
from tkinter import Canvas, Toplevel
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
        func(x1, y1, x2, y2, fill=color, outline=color)


def custom_alert(title, message):
    alert_window = Toplevel()
    alert_window.title(title)
    alert_window.geometry("400x200")
    alert_window.configure(bg="#FAFAFA")
    alert_window.resizable(False, False)
    alert_window.attributes("-topmost", True)

    def close_alert():
        alert_window.destroy()

    title_label = tk.Label(alert_window, text=title, font=("Helvetica", 16, "bold"), bg="#FAFAFA", fg="#FF4C4C")
    title_label.pack(pady=10)

    message_label = tk.Label(alert_window, text=message, font=("Helvetica", 12), bg="#FAFAFA", fg="#333333", wraplength=350)
    message_label.pack(pady=10)

    close_button = tk.Button(
        alert_window,
        text="OK",
        font=("Helvetica", 12),
        bg="#FF4C4C",
        fg="white",
        activebackground="#FF6666",
        activeforeground="white",
        relief="flat",
        command=close_alert,
    )
    close_button.pack(pady=10)

    alert_window.update_idletasks()
    window_width = alert_window.winfo_width()
    window_height = alert_window.winfo_height()
    screen_width = alert_window.winfo_screenwidth()
    screen_height = alert_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    alert_window.geometry(f"{window_width}x{window_height}+{x}+{y}")


def display_data(result_frame, data, city_name):
    try:
        components = data["list"][0]["components"]
        pm2_5_value = components["pm2_5"]
        pm10_value = components["pm10"]

        aqi = calculate_aqi(pm2_5_value, pm10_value)
        if aqi is None:
            return

        if aqi > 200:
            # Call custom alert
            custom_alert(
                "Bardzo niezdrowe powietrze",
                "Jakość powietrza jest bardzo niezdrowa! Pozostań w domu i unikaj wychodzenia na zewnątrz."
            )

        card_color, air_status = get_aqi_color_and_label(aqi)

        for widget in result_frame.winfo_children():
            widget.destroy()

        card_width, card_height = 600, 280
        c = Canvas(result_frame, width=card_width, height=card_height, bg="#FAFAFA", highlightthickness=0)
        c.pack(pady=20)

        card_center_x = card_width // 2
        card_center_y = card_height // 2
        draw_rounded_card(c, card_center_x, card_center_y, card_width - 20, card_height - 20, 30, card_color)

        # Fonts
        font_aqi_value = ("Helvetica", 36, "bold")
        font_aqi_label = ("Helvetica", 16)
        font_pm_value = ("Helvetica", 14, "bold")
        font_pm_label = ("Helvetica", 12)

        # AQI
        c.create_text(card_center_x - 250, card_center_y - 80, text=f"{aqi} AQI+", font=font_aqi_value, fill="#333333", anchor="w")
        c.create_text(card_center_x - 250, card_center_y - 40, text=air_status, font=font_aqi_label, fill="#333333", anchor="w")

        # Main pollutant
        main_pollutant = "PM2.5" if pm2_5_value > pm10_value else "PM10"
        main_pollutant_value = max(pm2_5_value, pm10_value)
        c.create_text(card_center_x + 50, card_center_y - 80, text="Główne źródło:", font=font_pm_label, fill="#111111", anchor="w")
        c.create_text(card_center_x + 50, card_center_y - 50, text=f"{main_pollutant}: {main_pollutant_value:.2f} µg/m³", font=font_pm_value, fill="#111111", anchor="w")

        # PM2.5 and PM10
        c.create_text(card_center_x - 250, card_center_y + 10, text="PM2.5:", font=font_pm_label, fill="#111111", anchor="w")
        c.create_text(card_center_x - 200, card_center_y + 10, text=f"{pm2_5_value:.2f} µg/m³", font=font_pm_value, fill="#111111", anchor="w")

        c.create_text(card_center_x + 50, card_center_y + 10, text="PM10:", font=font_pm_label, fill="#111111", anchor="w")
        c.create_text(card_center_x + 100, card_center_y + 10, text=f"{pm10_value:.2f} µg/m³", font=font_pm_value, fill="#111111", anchor="w")
    except (KeyError, IndexError, TypeError) as e:
        tk.messagebox.showerror("Błąd", f"Problem z przetwarzaniem danych: {e}")
