import requests
from datetime import datetime

API = '6074b2946d25ae8c032028ff26ac67f7'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast'

def get_weather(city):
    params = {
        "q": city,
        "appid": API,
        "units": "metric"
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        if response.status_code != 200:
            print(f"Error: {data.get('message', 'Unknown error occurred.')}")
            return None
        
        weather_data = {
            'Current':{
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"].capitalize(),
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"]
            },
            
            'Forecast': {}
        }
        
        forecast_response = requests.get(FORECAST_URL, params=params)
        forecast_data = forecast_response.json()

        shown_dates = set()
        forecast_days = {}

        for entry in forecast_data["list"]:
            dt_txt = entry["dt_txt"]
            date_obj = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")

            # Pick forecasts around 12:00 PM (or adjust to your preference)
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
        print("Exception occured:", e)
        return None

def main():
    print("\nWEATHER APP")
    print("\nEnter 'exit' to exit.")
    
    while True:
        city = input("Enter a city: ").strip()
        
        if city.lower() == "exit":
            print("See you next time!")
            break
        
        if not city:
            print("Enter a valid city name.")
            continue
        
        data = get_weather(city)
        
        if data:
            weather = data['Current']
            forecast = data['Forecast']
            
            print("\nCurrent Weather:")
            print(f"Location: {weather['city']}, {weather['country']}")
            print(f"Condition: {weather['description']}")
            print(f"Temperature: {weather['temperature']}°C")
            print(f"Humidity: {weather['humidity']}%")
            print(f"Wind Speed: {weather['wind_speed']} m/s")
            
            print('\n 3-Day Forecast:')
            for key, day in forecast.items():
                print(f"{day['date']}: {day['description']}, {day['temperature']}°C")
            
if __name__ == "__main__":
    main()