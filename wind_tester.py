import urllib.request
import json

url = (
    "https://api.open-meteo.com/v1/forecast?"
    "latitude=28.267118"
    "&longitude=-80.662580"
    "&hourly=wind_speed_10m,wind_gusts_10m,wind_direction_10m"
    "&wind_speed_unit=mph"
    "&timezone=America%2FNew_York"
    "&forecast_days=2"
    "&cell_selection=nearest"
)

response = urllib.request.urlopen(url)
data = json.load(response)

times = data["hourly"]["time"]
winds = data["hourly"]["wind_speed_10m"]
gusts = data["hourly"]["wind_gusts_10m"]
directions = data["hourly"]["wind_direction_10m"]

print("TODAY'S HOURLY WIND")
print("-------------------")

for i in range(len(times)):
    hour = int(times[i][11:13])

    if 8 <= hour <= 20:
        print(
            times[i],
            " Wind:", winds[i], "mph",
            " Gust:", gusts[i], "mph",
            " Direction:", directions[i]
        )
print()
print("API INFORMATION")
print("Latitude returned:", data.get("latitude"))
print("Longitude returned:", data.get("longitude"))
print("Elevation:", data.get("elevation"))
print("Timezone:", data.get("timezone"))
print("Timezone abbreviation:", data.get("timezone_abbreviation"))
print("UTC offset:", data.get("utc_offset_seconds"))
print("Generation time:", data.get("generationtime_ms"), "ms")
