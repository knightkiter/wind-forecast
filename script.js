const today = new Date();

const formattedToday = today.toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
    year: "numeric"
});

document.getElementById("today-heading").textContent =
    `Wind Forecast for Today — ${formattedToday}`;
const latitude = 28.267118;
const longitude = -80.662580;

const url =
    `https://api.open-meteo.com/v1/forecast?latitude=${latitude}` +
    `&longitude=${longitude}` +
    `&hourly=wind_speed_10m,wind_gusts_10m,wind_direction_10m` +
    `&wind_speed_unit=mph` +
    `&timezone=America%2FNew_York` +
    `&forecast_days=7` +
    `&cell_selection=nearest`;

function degreesToDirection(degrees) {
    const directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"];
    const index = Math.round(degrees / 45) % 8;
    return directions[index];
}

function formatTime(hour) {
    if (hour === 0) {
        return "12:00 AM";
    } else if (hour < 12) {
        return `${hour}:00 AM`;
    } else if (hour === 12) {
        return "12:00 PM";
    } else {
        return `${hour - 12}:00 PM`;
    }
}

async function loadForecast() {
    try {
        const response = await fetch(url);
        const data = await response.json();

        const times = data.hourly.time;
        const winds = data.hourly.wind_speed_10m;
        const gusts = data.hourly.wind_gusts_10m;
        const directions = data.hourly.wind_direction_10m;

        document.getElementById("forecast-status").textContent =
            "South Tropical Trail / Banana River";

        let todayHTML = `
            <table>
                <tr>
                    <th>Time</th>
                    <th>Wind</th>
                    <th>Gust</th>
                    <th>Dir</th>
                </tr>
        `;

        let bestWind = 0;
        let bestIndex = 8;

        for (let i = 8; i < 21; i++) {
            const hour = parseInt(times[i].substring(11, 13));
            const displayTime = formatTime(hour);
            const compass = degreesToDirection(directions[i]);

            if (winds[i] > bestWind) {
                bestWind = winds[i];
                bestIndex = i;
            }

            todayHTML += `
                <tr>
                    <td>${displayTime}</td>
                    <td>${winds[i]} mph</td>
                    <td>${gusts[i]} mph</td>
                    <td>${compass}</td>
                </tr>
            `;
        }

        todayHTML += "</table>";

        const bestHour = parseInt(times[bestIndex].substring(11, 13));
        const bestTime = formatTime(bestHour);
        const bestDirection = degreesToDirection(directions[bestIndex]);

        todayHTML += `
            <p>
                <strong>Best Wind:</strong>
                ${bestTime} - ${winds[bestIndex]} mph,
                gust ${gusts[bestIndex]} mph,
                ${bestDirection}
            </p>
        `;

        document.getElementById("today-forecast").innerHTML = todayHTML;

        let weekHTML = `
            <table>
                <tr>
                    <th>Day</th>
                    <th>Time</th>
                    <th>Wind</th>
                    <th>Gust</th>
                    <th>Dir</th>
                </tr>
        `;

        let weekBestWind = 0;
        let weekBestIndex = -1;

        for (let day = 0; day < 7; day++) {
            const start = day * 24 + 8;
            const end = day * 24 + 21;

            let dayBestIndex = start;

            for (let i = start; i < end; i++) {
                if (winds[i] > winds[dayBestIndex]) {
                    dayBestIndex = i;
                }
            }

            const rawTime = times[dayBestIndex];
            const date = new Date(rawTime);

            const dayName = date.toLocaleDateString("en-US", {
                weekday: "short",
                month: "short",
                day: "numeric"
            });

            const hour = parseInt(rawTime.substring(11, 13));
            const displayTime = formatTime(hour);
            const compass = degreesToDirection(directions[dayBestIndex]);

            const preferredDirections = ["NE", "E", "SE"];
            const candidatePreferred = preferredDirections.includes(compass);
            
            const currentBestPreferred =
            weekBestIndex !== -1 &&
            preferredDirections.includes(
                degreesToDirection(directions[weekBestIndex])
            );
        
        if (
            weekBestIndex === -1 ||
            (candidatePreferred && !currentBestPreferred) ||
            (candidatePreferred === currentBestPreferred &&
                winds[dayBestIndex] > weekBestWind)
        ) {
            weekBestWind = winds[dayBestIndex];
            weekBestIndex = dayBestIndex;
        }

            weekHTML += `
                <tr>
                    <td>${dayName}</td>
                    <td>${displayTime}</td>
                    <td>${winds[dayBestIndex]} mph</td>
                    <td>${gusts[dayBestIndex]} mph</td>
                    <td>${compass}</td>
                </tr>
            `;
        }

        weekHTML += "</table>";

        const bestDate = new Date(times[weekBestIndex]);

        const bestDayName = bestDate.toLocaleDateString("en-US", {
            weekday: "short",
            month: "short",
            day: "numeric"
        });

        const weekBestHour =
            parseInt(times[weekBestIndex].substring(11, 13));

        const weekBestTime = formatTime(weekBestHour);

        const weekBestDirection =
            degreesToDirection(directions[weekBestIndex]);

        weekHTML += `
            <p>
                <strong>Best Kiteboarding Forecast:</strong>
                ${bestDayName} ${weekBestTime} -
                ${winds[weekBestIndex]} mph,
                gust ${gusts[weekBestIndex]} mph,
                ${weekBestDirection}
            </p>
        `;

        document.getElementById("seven-day-forecast").innerHTML = weekHTML;

    } catch (error) {
        document.getElementById("forecast-status").textContent =
            "Unable to load forecast data.";

        console.error(error);
    }
}

loadForecast();
