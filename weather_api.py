import requests

API_KEY = "7339a5773cc67c6e58cb5365628cecaa"
city = "Mumbai"

url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

response = requests.get(url)
data = response.json()

# 🔍 Debug
print("API Response:", data)

# ✅ Check if API worked
if response.status_code == 200 and "main" in data:

    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"] * 3.6

    rainfall = 0
    if "rain" in data:
        rainfall = data["rain"].get("1h", 0)

    print("\n✅ Weather Data:")
    print("Temperature:", temperature)
    print("Humidity:", humidity)
    print("Wind Speed:", wind_speed)
    print("Rainfall:", rainfall)

else:
    print("\n❌ API Error:")
    print("Status Code:", response.status_code)
    print("Message:", data.get("message"))