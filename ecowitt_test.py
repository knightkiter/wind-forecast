import urllib.request
import urllib.parse
import json
import csv
from datetime import datetime

from ecowitt_secrets import API_KEY, APPLICATION_KEY


MAC = "FC:F5:C4:B3:0D:70"

params = {
    "application_key": APPLICATION_KEY,
    "api_key": API_KEY,
    "mac": MAC,
    "call_back": "wind",
    "wind_speed_unitid": "9"
}

url = "https://api.ecowitt.net/api/v3/device/real_time?" + urllib.parse.urlencode(params)

with urllib.request.urlopen(url) as response:
    data = json.load(response)


wind_data = data["data"]["wind"]

wind_speed = wind_data["wind_speed"]["value"]
wind_gust = wind_data["wind_gust"]["value"]
wind_direction = int(wind_data["wind_direction"]["value"])


def direction_name(degrees):
    directions = [
        "N", "NNE", "NE", "ENE",
        "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW",
        "W", "WNW", "NW", "NNW"
    ]

    index = round(degrees / 22.5) % 16
    return directions[index]


def reading_quality(degrees):
    if 22.5 <= degrees <= 157.5:
        return "USABLE"
    else:
        return "LIMITED"


print()
print("SOUTH TROPICAL TRAIL - ECOWITT")
print("==============================")
print(f"Wind:      {wind_speed} mph")
print(f"Gust:      {wind_gust} mph")
print(f"Direction: {wind_direction}° ({direction_name(wind_direction)})")
print(f"Station reading: {reading_quality(wind_direction)}")
csv_file = "ecowitt_observations.csv"

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
quality = reading_quality(wind_direction)

try:
    with open(csv_file, "x", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Date_Time",
            "Wind_mph",
            "Gust_mph",
            "Direction_degrees",
            "Direction",
            "Quality"
        ])
except FileExistsError:
    pass

with open(csv_file, "a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([
        timestamp,
        wind_speed,
        wind_gust,
        wind_direction,
        direction_name(wind_direction),
        quality
    ])

print()
print("Observation saved to ecowitt_observations.csv")