import urllib.request
import json
from datetime import datetime

url = "https://api.open-meteo.com/v1/gfs?latitude=28.267118&longitude=-80.662580&hourly=wind_speed_10m,wind_gusts_10m,wind_direction_10m&wind_speed_unit=mph&timezone=America%2FNew_York&forecast_days=7&cell_selection=sea"

response = urllib.request.urlopen(url)
data = json.load(response)


def degrees_to_direction(degrees):
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = round(degrees / 45) % 8
    return directions[index]


# TODAY'S HOURLY FORECAST
today = datetime.now()
today_text = today.strftime("%A %b %d, %Y")

print()
print("SOUTH TROPICAL TRAIL FORECAST")
print("TODAY:", today_text)
print("Merritt Island, Florida")
print()
print("TIME      WIND       GUST       DIR")
print("------------------------------------")

best_wind = 0
best_time = ""
best_gust = 0
best_direction = ""

for i in range(8, 21):
    raw_time = data["hourly"]["time"][i]
    hour = int(raw_time[11:13])

    if hour == 0:
        display_time = "12:00 AM"
    elif hour < 12:
        display_time = f"{hour}:00 AM"
    elif hour == 12:
        display_time = "12:00 PM"
    else:
        display_time = f"{hour - 12}:00 PM"

    wind = data["hourly"]["wind_speed_10m"][i]
    gust = data["hourly"]["wind_gusts_10m"][i]
    direction = data["hourly"]["wind_direction_10m"][i]
    compass = degrees_to_direction(direction)

    if wind > best_wind:
        best_wind = wind
        best_time = display_time
        best_gust = gust
        best_direction = compass

    print(
        f"{display_time:<9} "
        f"{wind:>4} mph   "
        f"{gust:>4} mph   "
        f"{compass}"
    )

print()
print(
    "BEST WIND:",
    best_time,
    "-",
    best_wind,
    "mph, gust",
    best_gust,
    "mph,",
    best_direction
)


# 7-DAY FORECAST
print()
print("7-DAY BEST WIND FORECAST")
print()

times = data["hourly"]["time"]
winds = data["hourly"]["wind_speed_10m"]
gusts = data["hourly"]["wind_gusts_10m"]
directions = data["hourly"]["wind_direction_10m"]

print("DAY         TIME       WIND       GUST       DIR")
print("------------------------------------------------")

week_best_wind = 0
week_best_date = ""
week_best_time = ""
week_best_gust = 0
week_best_direction = ""

for day in range(7):
    start = day * 24 + 8
    end = day * 24 + 21

    best_index = start

    for i in range(start, end):
        if winds[i] > winds[best_index]:
            best_index = i

    raw_time = times[best_index]

    date_object = datetime.strptime(raw_time[:10], "%Y-%m-%d")
    date = date_object.strftime("%a %b %d")

    hour = int(raw_time[11:13])

    if hour == 0:
        display_time = "12:00 AM"
    elif hour < 12:
        display_time = f"{hour}:00 AM"
    elif hour == 12:
        display_time = "12:00 PM"
    else:
        display_time = f"{hour - 12}:00 PM"

    compass = degrees_to_direction(directions[best_index])

    if winds[best_index] > week_best_wind:
        week_best_wind = winds[best_index]
        week_best_date = date
        week_best_time = display_time
        week_best_gust = gusts[best_index]
        week_best_direction = compass

    print(
        f"{date:<11} "
        f"{display_time:<10} "
        f"{winds[best_index]:>4} mph   "
        f"{gusts[best_index]:>4} mph   "
        f"{compass}"
    )

print()
print(
    "BEST DAY THIS WEEK:",
    week_best_date,
    week_best_time,
    "-",
    week_best_wind,
    "mph, gust",
    week_best_gust,
    "mph,",
    week_best_direction
)