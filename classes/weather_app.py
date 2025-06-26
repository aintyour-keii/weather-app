import requests
from datetime import datetime, date

class WeatherApp:
    def __init__(self):
        self.api_key = '6074b2946d25ae8c032028ff26ac67f7'
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        
    def get_weather(self, city):
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        
        try:
            # --- Current Weather ---
            current_response = requests.get(self.base_url, params=params)
            current_data = current_response.json()

            if current_response.status_code != 200:
                print(f"Error: {current_data.get('message', 'Unknown error occurred.')}")
                return None

            weather_data = {
                'Current': {
                    "city": current_data["name"],
                    "country": current_data["sys"]["country"],
                    "temperature": current_data["main"]["temp"],
                    "description": current_data["weather"][0]["description"].capitalize(),
                    "humidity": current_data["main"]["humidity"],
                    "wind_speed": current_data["wind"]["speed"]
                },
                'Forecast': {}
            }

            # --- 3-Day Forecast ---
            forecast_response = requests.get(self.forecast_url, params=params)
            forecast_data = forecast_response.json()

            shown_dates = set()
            forecast_days = {}
            today = date.today()

            for entry in forecast_data["list"]:
                dt_txt = entry["dt_txt"]
                date_obj = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")

                if date_obj.date() == today:
                    continue

                if date_obj.hour == 12 and date_obj.date() not in shown_dates:
                    day_key = f"day_{len(shown_dates) + 1}"
                    forecast_days[day_key] = {
                        "date": date_obj.strftime("%A, %b %d"),
                        "description": entry["weather"][0]["description"].capitalize(),
                        "temperature": entry["main"]["temp"]
                    }
                    shown_dates.add(date_obj.date())

                    if len(shown_dates) >= 3:
                        break

            weather_data["Forecast"] = forecast_days

            return weather_data

        except Exception as e:
            print("Exception occurred:", e)
            return None
        
    def display_weather(self, weather_data):
        current = weather_data["Current"]
        print("\nCurrent Weather:")
        print(f"{current['city']}, {current['country']}")
        print(f"{current['description']}")
        print(f"Temperature: {current['temperature']}°C")
        print(f"Humidity: {current['humidity']}%")
        print(f"Wind Speed: {current['wind_speed']} m/s")

        print("\n3-Day Forecast:")
        for day in weather_data["Forecast"].values():
            print(f"{day['date']}: {day['description']}, {day['temperature']}°C")

    def run(self):
        print("\nWeather App")
        print("Enter: 'exit' to exit the app.")
        while True:
            city = input("\n🌍 Enter a city name: ").strip()
            if city.lower() == "exit":
                print("👋 Goodbye!")
                break

            if not city:
                print("⚠️ Please enter a valid city name.")
                continue

            data = self.get_weather(city)
            if data:
                self.display_weather(data)