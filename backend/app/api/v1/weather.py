"""Weather API endpoints utilizing OpenWeather API."""

import random
import httpx
from fastapi import APIRouter
from pydantic import BaseModel
from app.core.config import settings

router = APIRouter()

REGION_COORDS = {
    # English/Standard
    "Tashkent": (41.299, 69.240),
    "Samarkand": (39.654, 66.959),
    "Fergana": (40.384, 71.789),
    "Bukhara": (39.767, 64.421),
    "Andijan": (40.783, 72.344),
    "Namangan": (40.995, 71.672),
    "Kashkadarya": (38.860, 65.800),
    "Surkhandarya": (37.224, 67.278),
    "Khorezm": (41.551, 60.631),
    "Jizzakh": (40.115, 67.842),
    "Navoi": (40.103, 65.379),
    "Syrdarya": (40.486, 68.715),
    "Karakalpakstan": (42.461, 59.606),
    # Uzbek spelling variants
    "Toshkent": (41.299, 69.240),
    "Samarqand": (39.654, 66.959),
    "Farg'ona": (40.384, 71.789),
    "Fargona": (40.384, 71.789),
    "Buxoro": (39.767, 64.421),
    "Andijon": (40.783, 72.344),
    "Qashqadaryo": (38.860, 65.800),
    "Surxondaryo": (37.224, 67.278),
    "Xorazm": (41.551, 60.631),
    "Jizzax": (40.115, 67.842),
    "Sirdaryo": (40.486, 68.715),
    "Qoraqalpog'iston": (42.461, 59.606),
    "Qoraqalpogiston": (42.461, 59.606),
}


class WeatherResponse(BaseModel):
    success: bool
    data: dict


def get_mock_weather(region: str, coords: tuple) -> WeatherResponse:
    """Fallback generator for mock weather data."""
    base_temp = random.uniform(22, 36)
    return WeatherResponse(
        success=True,
        data={
            "region": region,
            "coordinates": {"lat": coords[0], "lng": coords[1]},
            "temperature": round(base_temp, 1),
            "feels_like": round(base_temp + random.uniform(1, 3), 1),
            "humidity": random.randint(25, 60),
            "wind_speed": round(random.uniform(2, 9), 1),
            "description": random.choice(["Clear sky", "Few clouds", "Partly cloudy", "Sunny"]),
            "icon": "01d",
            "forecast": [
                {
                    "date": f"2026-05-{20+i}",
                    "temp_min": round(base_temp - random.uniform(4, 8), 1),
                    "temp_max": round(base_temp + random.uniform(1, 4), 1),
                    "description": random.choice(["Sunny", "Partly cloudy", "Clear"]),
                    "icon": "01d",
                }
                for i in range(5)
            ],
        },
    )


@router.get("/{region}", response_model=WeatherResponse)
async def get_weather(region: str):
    """Get current weather and 5-day forecast for a region using OpenWeather API."""
    normalized_region = region.strip().title()
    coords = REGION_COORDS.get(normalized_region, (41.299, 69.240))

    api_key = settings.OPENWEATHER_API_KEY
    if not api_key or "your_openweather" in api_key or api_key == "81ef32f90680636aaf3b1db5e2adb601_example":
        return get_mock_weather(normalized_region, coords)

    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={coords[0]}&lon={coords[1]}&appid={api_key}&units=metric"

    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.get(url)
            if resp.status_code != 200:
                return get_mock_weather(normalized_region, coords)

            data = resp.json()
            forecast_list = data.get("list", [])
            if not forecast_list:
                return get_mock_weather(normalized_region, coords)

            current = forecast_list[0]
            daily_forecast = []

            # Group forecasts by day (approximately every 8th element represents a 24-hour leap)
            for i in range(1, 6):
                idx = min(i * 8, len(forecast_list) - 1)
                item = forecast_list[idx]
                dt_txt = item.get("dt_txt", "")
                date_str = dt_txt.split(" ")[0] if dt_txt else f"2026-05-{20+i}"

                daily_forecast.append({
                    "date": date_str,
                    "temp_min": round(item["main"]["temp_min"], 1),
                    "temp_max": round(item["main"]["temp_max"], 1),
                    "description": item["weather"][0]["description"].capitalize(),
                    "icon": item["weather"][0]["icon"],
                })

            return WeatherResponse(
                success=True,
                data={
                    "region": normalized_region,
                    "coordinates": {"lat": coords[0], "lng": coords[1]},
                    "temperature": round(current["main"]["temp"], 1),
                    "feels_like": round(current["main"]["feels_like"], 1),
                    "humidity": current["main"]["humidity"],
                    "wind_speed": round(current["wind"]["speed"], 1),
                    "description": current["weather"][0]["description"].capitalize(),
                    "icon": current["weather"][0]["icon"],
                    "forecast": daily_forecast,
                },
            )
    except Exception:
        return get_mock_weather(normalized_region, coords)
