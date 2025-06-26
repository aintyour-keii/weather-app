import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from classes.weather_app import WeatherApp

class WeatherGui:
    def __init__(self):
        self.weather_app = WeatherApp()

        self.root = tk.Tk()
        self.root.title("Weather App")
        self.root.geometry("450x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e1e")  # Dark background

        self.current_icon_image = None
        self.forecast_icon_images = [None, None, None]

        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Global Label Style
        self.style.configure("TLabel",
            background="#2c2c2c",
            foreground="#e0e0e0",
            font=("Segoe UI", 11)
        )

        # Header Label
        self.style.configure("Header.TLabel",
            background="#1e1e1e",
            foreground="#ffffff",
            font=("Segoe UI", 18, "bold")
        )

        # Entry Style
        self.style.configure("TEntry",
            font=("Segoe UI", 11),
            padding=5,
            relief="flat",
            borderwidth=2,
            fieldbackground="#2c2c2c",
            foreground="#e0e0e0"
        )
        self.style.map("TEntry",
            fieldbackground=[("focus", "#3a3a3a")],
            foreground=[("focus", "#ffffff")]
        )

        # Button Style
        self.style.configure("TButton",
            font=("Segoe UI", 11, "bold"),
            foreground="#ffffff",
            background="#3a72d8",
            padding=(15, 8),
            relief="flat",
            borderwidth=0
        )
        self.style.map("TButton",
            background=[("active", "#2a52b2"), ("pressed", "#2a52b2")],
            foreground=[("active", "#ffffff"), ("pressed", "#ffffff")]
        )

        # Frame Styles
        self.style.configure("TFrame", background="#1e1e1e")
        self.style.configure("Card.TFrame",
            background="#2c2c2c",
            relief="flat",
            borderwidth=1,
            bordercolor="#444444"
        )

        self.setup_widgets()

    def setup_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.grid_columnconfigure(0, weight=1)

        header_label = ttk.Label(main_frame, text="Weather Forecast", style="Header.TLabel")
        header_label.grid(row=0, column=0, pady=(0, 25), sticky="n")

        input_frame = ttk.Frame(main_frame, padding=15, style="Card.TFrame")
        input_frame.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)

        city_label = ttk.Label(input_frame, text="Enter City Name:", font=("Segoe UI", 12, "bold"))
        city_label.grid(row=0, column=0, pady=(0, 10), sticky="w")

        self.city_entry = ttk.Entry(input_frame, width=30)
        self.city_entry.grid(row=1, column=0, pady=(0, 15), sticky="ew")
        self.city_entry.bind("<Return>", lambda event=None: self.fetch_weather())

        get_button = ttk.Button(input_frame, text="Get Weather", command=self.fetch_weather)
        get_button.grid(row=2, column=0, pady=(0, 5), sticky="ew")

        self.current_weather_frame = ttk.Frame(main_frame, padding=15, style="Card.TFrame")
        self.current_weather_frame.grid(row=2, column=0, pady=(0, 20), sticky="ew")
        self.current_weather_frame.grid_columnconfigure(0, weight=1)
        self.current_weather_frame.grid_columnconfigure(1, weight=1)

        self.current_city_label = ttk.Label(self.current_weather_frame, text="", font=("Segoe UI", 14, "bold"),
                                            foreground="#e0e0e0")
        self.current_city_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")

        self.current_icon_label = ttk.Label(self.current_weather_frame)
        self.current_icon_label.grid(row=1, column=0, rowspan=3, padx=(0, 15), sticky="w")

        self.current_temp_label = ttk.Label(self.current_weather_frame, text="", font=("Segoe UI", 24, "bold"),
                                            foreground="#e74c3c")
        self.current_temp_label.grid(row=1, column=1, sticky="w")

        self.current_desc_label = ttk.Label(self.current_weather_frame, text="", font=("Segoe UI", 12))
        self.current_desc_label.grid(row=2, column=1, sticky="w")

        self.current_details_label = ttk.Label(self.current_weather_frame, text="", font=("Segoe UI", 11))
        self.current_details_label.grid(row=3, column=1, sticky="w")

        self.forecast_frame = ttk.Frame(main_frame, padding=15, style="Card.TFrame")
        self.forecast_frame.grid(row=3, column=0, pady=(0, 5), sticky="ew")
        self.forecast_frame.grid_columnconfigure(0, weight=1)
        self.forecast_frame.grid_columnconfigure(1, weight=1)
        self.forecast_frame.grid_columnconfigure(2, weight=1)

        forecast_title_label = ttk.Label(self.forecast_frame, text="3-Day Forecast:",
                                         font=("Segoe UI", 12, "bold"), foreground="#e0e0e0")
        forecast_title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="w")

        self.forecast_labels = []
        for i in range(3):
            day_frame = ttk.Frame(self.forecast_frame, style="Card.TFrame")
            day_frame.grid(row=i + 1, column=0, columnspan=3, sticky="ew", pady=5)
            day_frame.grid_columnconfigure(0, weight=1)
            day_frame.grid_columnconfigure(1, weight=2)
            day_frame.grid_columnconfigure(2, weight=1)
            day_frame.grid_columnconfigure(3, weight=1)

            date_label = ttk.Label(day_frame, text="", font=("Segoe UI", 10, "bold"), foreground="#5d6d7e")
            date_label.grid(row=0, column=0, sticky="w")

            desc_label = ttk.Label(day_frame, text="", font=("Segoe UI", 10), foreground="#5d6d7e")
            desc_label.grid(row=0, column=1, sticky="w")

            temp_label = ttk.Label(day_frame, text="", font=("Segoe UI", 10, "bold"), foreground="#e74c3c")
            temp_label.grid(row=0, column=2, sticky="e")

            icon_label = ttk.Label(day_frame)
            icon_label.grid(row=0, column=3, padx=(10, 0), sticky="e")

            self.forecast_labels.append({
                "date": date_label,
                "desc": desc_label,
                "temp": temp_label,
                "icon": icon_label
            })

    def fetch_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showerror("Error", "Please enter a city name.")
            return

        self.clear_weather_display()

        self.current_city_label.config(text=f"Loading weather for {city}...")
        self.root.update_idletasks()

        data = self.weather_app.get_weather(city)

        if not data:
            messagebox.showerror("Error", f"Could not fetch weather for {city}. Please check the city name.")
            self.clear_weather_display()
            return

        self.display_weather(data)

    def display_weather(self, data):
        current = data['Current']
        forecast = data['Forecast']

        self.current_city_label.config(text=f"{current['city']}, {current['country']}")
        self.current_temp_label.config(text=f"{current['temperature']}°C")
        self.current_desc_label.config(text=f"{current['description'].capitalize()}")
        self.current_details_label.config(text=f"Humidity: {current['humidity']}%\nWind: {current['wind_speed']} m/s")

        current_icon_path = os.path.join("assets", "icons", current['icon'])  # PNG filename
        print(current_icon_path)
        icon_img = Image.open(current_icon_path).resize((64, 64))
        self.current_icon_image = ImageTk.PhotoImage(icon_img)
        self.current_icon_label.config(image=self.current_icon_image)

        for i, day_key in enumerate(forecast.keys()):
            day = forecast[day_key]
            self.forecast_labels[i]["date"].config(text=f"{day['date']}")
            self.forecast_labels[i]["desc"].config(text=f"{day['description'].capitalize()}")
            self.forecast_labels[i]["temp"].config(text=f"{day['temperature']}°C")

            forecast_icon_path = os.path.join("assets", "icons", day['icon'])
            forecast_img = Image.open(forecast_icon_path).resize((32, 32))
            self.forecast_icon_images[i] = ImageTk.PhotoImage(forecast_img)
            self.forecast_labels[i]["icon"].config(image=self.forecast_icon_images[i])

    def clear_weather_display(self):
        self.current_city_label.config(text="")
        self.current_icon_label.config(image="")
        self.current_temp_label.config(text="")
        self.current_desc_label.config(text="")
        self.current_details_label.config(text="")

        for label_set in self.forecast_labels:
            label_set["date"].config(text="")
            label_set["desc"].config(text="")
            label_set["temp"].config(text="")
            label_set["icon"].config(image="")

    def run(self):
        self.root.mainloop()
