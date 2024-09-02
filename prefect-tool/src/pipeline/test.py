from pprint import pprint

import requests

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 40.7128,
    "longitude": -74.005999,
    "current_weather": True,
    "current": [
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "wind_speed_10m",
    ],
    "daily": ["temperature_2m_max", "temperature_2m_min"],
    "forecast_days": 1,
}

response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    weather_data = response.json()
    pprint(weather_data)
else:
    print(f"Error: {response.status_code}")
