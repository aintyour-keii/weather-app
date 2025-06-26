import requests

API = '6074b2946d25ae8c032028ff26ac67f7'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

def get_weather(city):
    completed_url = BASE_URL+ f"?{city}&appid={API}&units=metric"
    
    try:
        response = requests.get(completed_url)
        data = response.json()
        
        if response.status_code != 200:
            print(f"Error: {data.get('message', 'Unknown error occurred.')}")
            return None
        
        weather_data = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"].capitalize(),
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
        
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
        
        weather = get_weather(city)
        
        if weather:
            print("\nCurrent Weather:")
            print(f"Location: {weather['city']}, {weather['country']}")
            print(f"Condition: {weather['description']}")
            print(f"Temperature: {weather['temperature']}°C")
            print(f"Humidity: {weather['humidity']}%")
            print(f"Wind Speed: {weather['wind_speed']} m/s")
            
if __name__ == "__main__":
    main()