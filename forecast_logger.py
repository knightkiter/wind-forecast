import urllib.request
import urllib.parse
import json
import csv
from datetime import datetime


LATITUDE = 28.267118
LONGITUDE = -80.662580

params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": "wind_speed_10m,wind_gusts_10m,wind_direction_10m",
    "wind_speed_unit": "mph",
    "timezone": "America/New_York",
    "forecast_days": 1
}

url = (
    "https://api.open-meteo.com/v1/forecast?"
    + urllib.parse.urlencode(params)
)

with urllib.request.urlopen(url) as response:
    data = json.load(response)

times = data["hourly"]["time"]
winds = data["hourly"]["wind_speed_10m"]
gusts = data["hourly"]["wind_gusts_10m"]
directions = data["hourly"]["wind_direction_10m"]

csv_file = "openmeteo_forecasts.csv"

forecast_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

try:
    with open(csv_file, "x", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Forecast_Created",
            "Forecast_For",
            "Wind_mph",
            "Gust_mph",
            "Direction_degrees"
        ])
except FileExistsError:
    pass

with open(csv_file, "a", newline="") as file:
    writer = csv.writer(file)

    for i in range(len(times)):
        hour = int(times[i][11:13])

        if 8 <= hour <= 20:
            writer.writerow([
                forecast_created,
                times[i],
                winds[i],
                gusts[i],
                directions[i]
            ])

print()
print("OPEN-METEO FORECAST SNAPSHOT")
print("============================")
print(f"Forecast saved at: {forecast_created}")
print("Hourly forecasts from 8 AM through 8 PM saved.")
print("File: openmeteo_forecasts.csv")