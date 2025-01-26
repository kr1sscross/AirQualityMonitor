import tkinter as tk
from tkinter import messagebox
from api_utils import get_coordinates, get_air_quality
from gui_utils import display_data


def fetch_data():
    city_name = city_entry.get().strip()
    if city_name:
        coords = get_coordinates(city_name)
        if coords:
            lat, lon, name = coords
            air_quality_data = get_air_quality(lat, lon)
            if air_quality_data:
                display_data(result_frame, air_quality_data, name)
    else:
        messagebox.showerror("Błąd", "Podaj nazwę miasta.")


window = tk.Tk()
window.title("Monitor Jakości Powietrza")
window.geometry("800x500")
window.configure(bg="#FAFAFA")

top_frame = tk.Frame(window, bg="#FAFAFA")
top_frame.pack(side=tk.TOP, pady=20, fill="x")

city_frame = tk.Frame(top_frame, bg="#FAFAFA")
city_frame.pack(pady=10)

city_entry = tk.Entry(city_frame, font=("Helvetica", 14), width=40, relief="flat", bg="#F4F4F4", fg="#555555")
city_entry.insert(0, "Wpisz nazwę miasta")
city_entry.pack(side=tk.LEFT, ipady=5, padx=(10, 0))

city_entry.bind("<FocusIn>", lambda e: city_entry.delete(0, tk.END) if city_entry.get() == "Wpisz nazwę miasta" else None)
city_entry.bind("<FocusOut>", lambda e: city_entry.insert(0, "Wpisz nazwę miasta") if not city_entry.get() else None)

fetch_button = tk.Button(
    city_frame, text="🔍", font=("Helvetica", 14),
    bg="#EFEFEF", fg="#333333", activebackground="#DFDFDF", activeforeground="#111111",
    relief="flat", borderwidth=0, command=fetch_data
)
fetch_button.pack(side=tk.LEFT, padx=(5, 10))

result_frame = tk.Frame(window, bg="#FAFAFA")
result_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

window.mainloop()