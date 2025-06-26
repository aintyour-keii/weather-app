import tkinter as tk
from tkinter import ttk, messagebox
from classes.weather_app import WeatherApp

class WeatherGui:
    def __init__(self):
        self.weather_app = WeatherApp()
        
        self.root = tk.Tk()
        self.root.title("Weather App")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        
        self.setup_widgets()
        
    def setup_widgets(self):
        self.city_label = ttk.Label(self.root, text="Enter City: ")
        self.city_label.pack(pady=10)
        
        self.city_entry = ttk.Entry(self.root, width=30)
        self.city_entry.pack()

        self.get_button = ttk.Button(self.root, text="Get Weather", command=self.fetch_weather)
        self.get_button.pack(pady=10)

        self.result_text = tk.Text(self.root, width=40, height=20, state="disabled")
        self.result_text.pack(pady=10)
        
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