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

        self.get_button = ttk.Button(self.root, text="Get Weather")
        self.get_button.pack(pady=10)

        self.result_text = tk.Text(self.root, width=40, height=20, state="disabled")
        self.result_text.pack(pady=10)