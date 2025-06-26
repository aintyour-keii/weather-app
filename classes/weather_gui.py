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