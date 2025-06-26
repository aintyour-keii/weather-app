import tkinter as tk
from tkinter import ttk, messagebox
from classes.weather_app import WeatherApp

class WeatherGui:
    def __init__(self):
        self.weather_app = WeatherApp()
        
        self.root = tk.Tk()
        self.root.title("Weather App")
        self.root.geometry("420x540")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f2f5")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TLabel", background = "#f0f2f5", font = ("Segoe UI", 11))
        self.style.configure("TButton", font = ("Segoe UI", 10, "bold"))
        self.style.configure("TEntry", font = ("Segoe UI", 11))
        
        self.setup_widgets()
        
    def setup_widgets(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.city_label = ttk.Label(frame, text="Enter City: ")
        self.city_label.pack(anchor="w", pady=(0, 4))
        
        self.city_entry = ttk.Entry(frame, width=30)
        self.city_entry.pack(pady=(0, 10))

        self.get_button = ttk.Button(frame, text="Get Weather", command=self.fetch_weather)
        self.get_button.pack(pady=(0, 20))

        self.result_text = tk.Text(frame, width=40, height=20, state="disabled", bg="#ddd4cf", font=("Consolas", 10), relief="flat", wrap="word")
        self.result_text.pack()
        
    def fetch_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showerror("Error", f"Please enter a city name.")
            return
        
        data = self.weather_app.get_weather(city)
        if not data:
            messagebox.showerror("Error", f"Could not fetch weather for {city}.")
            return
        
        self.display_weather(data)
        
    def display_weather(self, data):
        self.result_text.configure(state='normal')
        self.result_text.delete(1.0, tk.END)

        current = data['Current']
        forecast = data['Forecast']

        self.result_text.insert(tk.END, f"📍 {current['city']}, {current['country']}\n")
        self.result_text.insert(tk.END, f"⛅ {current['description']}\n")
        self.result_text.insert(tk.END, f"🌡 Temp: {current['temperature']}°C\n")
        self.result_text.insert(tk.END, f"💧 Humidity: {current['humidity']}%\n")
        self.result_text.insert(tk.END, f"🌬 Wind: {current['wind_speed']} m/s\n\n")

        self.result_text.insert(tk.END, "📅 3-Day Forecast:\n")
        for day in forecast.values():
            self.result_text.insert(
                tk.END,
                f"{day['date']}: {day['description']}, {day['temperature']}°C\n"
            )

        self.result_text.configure(state='disabled')

    def run(self):
        self.root.mainloop()