import tkinter as tk
from tkinter import ttk, messagebox
from classes.weather_app import WeatherApp

class WeatherGui:
    def __init__(self):
        self.weather_app = WeatherApp()
        
        self.root = tk.Tk()
        self.root.title("Weather App")
        self.root.geometry("450x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#e0e5ec")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TLabel", background = "#e0e5ec", font = ("Segoe UI", 11))
        self.style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#2c3e50")
        self.style.configure("TEntry", font=("Segoe UI", 11), padding=5, relief="flat", borderwidth=2,fieldbackground="#ffffff", foreground="#34495e")
        self.style.map("TEntry", fieldbackground=[('focus', '#e0f7fa')])
        self.style.configure("TButton", font=("Segoe UI", 11, "bold"), foreground="#ffffff", background="#3498db", padding=(15, 8), relief="flat", borderwidth=0, bordercolor="#3498db")
        self.style.map("TButton", background=[('active', '#2980b9'), ('pressed', '#2980b9')], foreground=[('active', '#ffffff'), ('pressed', '#ffffff')])
        self.style.configure("TFrame", background="#e0e5ec")
        self.style.configure("Card.TFrame", background="#ffffff", relief="flat", borderwidth=1, bordercolor="#d0d0d0")
        
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
        
        self.current_city_label = ttk.Label(self.current_weather_frame, text="", font=("Segoe UI", 14, "bold"), foreground="#34495e")
        self.current_city_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")
        
        self.current_icon_label = ttk.Label(self.current_weather_frame, text="", font=("Segoe UI", 48))
        self.current_icon_label.grid(row=1, column=0, rowspan=3, padx=(0, 15), sticky="w")
        
        self.current_temp_label = ttk.Label(self.current_weather_frame, text="", font=("Segoe UI", 24, "bold"), foreground="#e74c3c")
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
        
        forecast_title_label = ttk.Label(self.forecast_frame, text="3-Day Forecast:", font=("Segoe UI", 12, "bold"), foreground="#34495e")
        forecast_title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="w")

        self.forecast_labels = []
        for i in range(3):
            day_frame = ttk.Frame(self.forecast_frame, style="TFrame")
            day_frame.grid(row=i+1, column=0, columnspan=3, sticky="ew", pady=5)
            day_frame.grid_columnconfigure(0, weight=1)
            day_frame.grid_columnconfigure(1, weight=2)
            day_frame.grid_columnconfigure(2, weight=1)

            date_label = ttk.Label(day_frame, text="", font=("Segoe UI", 10, "bold"), foreground="#5d6d7e")
            date_label.grid(row=0, column=0, sticky="w")

            desc_label = ttk.Label(day_frame, text="", font=("Segoe UI", 10), foreground="#5d6d7e")
            desc_label.grid(row=0, column=1, sticky="w")
            
            temp_label = ttk.Label(day_frame, text="", font=("Segoe UI", 10, "bold"), foreground="#e74c3c")
            temp_label.grid(row=0, column=2, sticky="e")
            
            self.forecast_labels.append({"date": date_label, "desc": desc_label, "temp": temp_label})

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
        self.current_icon_label.config(text=current['icon'])
        self.current_temp_label.config(text=f"{current['temperature']}°C")
        self.current_desc_label.config(text=current['description'].capitalize())
        self.current_details_label.config(text=f"Humidity: {current['humidity']}%\nWind: {current['wind_speed']} m/s")

        for i, day_key in enumerate(forecast.keys()):
            day = forecast[day_key]
            self.forecast_labels[i]["date"].config(text=f"{day['date']}")
            self.forecast_labels[i]["desc"].config(text=f"{day['description'].capitalize()}")
            self.forecast_labels[i]["temp"].config(text=f"{day['temperature']}°C {day['icon']}")

    def clear_weather_display(self):
        self.current_city_label.config(text="")
        self.current_icon_label.config(text="")
        self.current_temp_label.config(text="")
        self.current_desc_label.config(text="")
        self.current_details_label.config(text="")

        for label_set in self.forecast_labels:
            label_set["date"].config(text="")
            label_set["desc"].config(text="")
            label_set["temp"].config(text="")

    def run(self):
        self.root.mainloop()