import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from api_utils import coordinates, air_quality_data
from gui_utils import display_data


def fetch_data() -> None:
    city_name = entry.get().strip()

    if not city_name:
        CTkMessagebox(title="Error", message="Enter a city name.", icon="warning")
        return

    coords = coordinates(city_name)

    if coords is None:
        return

    lat, lon, city_name = coords

    air_quality_data2 = air_quality_data(lat, lon)

    if air_quality_data2 is None:
        return

    display_data(frame, air_quality_data2, city_name)


app = ctk.CTk()
app.title("Air Quality Monitor")
app.geometry("800x500")

search = ctk.CTkFrame(app, fg_color="transparent")
search.place(relx=0.5, rely=0.1, anchor="center")

entry = ctk.CTkEntry(search, placeholder_text="Enter a city name", width=300)
entry.grid(row=0, column=0, padx=(0, 10))

button = ctk.CTkButton(search, text="🔍", width=50, command=fetch_data)
button.grid(row=0, column=1)

frame = ctk.CTkFrame(app, fg_color="transparent", width=600, height=280, corner_radius=25)
frame.place(relx=0.5, rely=0.55, anchor="center")

app.mainloop()
