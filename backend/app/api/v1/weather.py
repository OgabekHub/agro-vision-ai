"""Weather API endpoints."""

import random
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

REGION_COORDS = {
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
}


class WeatherResponse(BaseModel):
    success: bool
    data: dict


@router.get("/{region}", response_model=WeatherResponse)
async def get_weather(region: str):
    """Get current weather for a region. Uses OpenWeather API in production."""
    coords = REGION_COORDS.get(region, (41.299, 69.240))

    # Mock weather data (in production, call OpenWeather API)
    base_temp = random.uniform(25, 38)
    return WeatherResponse(
        success=True,
        data={
            "region": region,
            "coordinates": {"lat": coords[0], "lng": coords[1]},
            "temperature": round(base_temp, 1),
            "feels_like": round(base_temp + random.uniform(1, 4), 1),
            "humidity": random.randint(20, 65),
            "wind_speed": round(random.uniform(2, 12), 1),
            "description": random.choice(["Clear sky", "Few clouds", "Scattered clouds", "Sunny"]),
            "icon": "01d",
            "forecast": [
                {
                    "date": f"2026-05-{17+i}",
                    "temp_min": round(base_temp - random.uniform(5, 10), 1),
                    "temp_max": round(base_temp + random.uniform(1, 5), 1),
                    "description": random.choice(["Sunny", "Partly cloudy", "Clear"]),
                    "icon": "01d",
                }
                for i in range(5)
            ],
        },
    )
