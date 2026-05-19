"""Regions API endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

REGIONS = [
    {"id": "tashkent", "name": "Tashkent", "name_uz": "Toshkent", "capital": "Tashkent", "coordinates": [41.299, 69.240], "area_km2": 15300, "climate": "Continental, Semi-arid", "avg_temperature": {"summer": 36, "winter": -2}, "annual_rainfall_mm": 440, "main_crops": ["Cotton", "Wheat", "Vegetables", "Grapes", "Fruits"], "soil_types": ["Loamy", "Sierozem"], "agricultural_area_hectares": 420000},
    {"id": "samarkand", "name": "Samarkand", "name_uz": "Samarqand", "capital": "Samarkand", "coordinates": [39.654, 66.959], "area_km2": 16400, "climate": "Continental", "avg_temperature": {"summer": 35, "winter": -1}, "annual_rainfall_mm": 350, "main_crops": ["Cotton", "Wheat", "Silk", "Grapes", "Melons"], "soil_types": ["Sierozem", "Alluvial"], "agricultural_area_hectares": 510000},
    {"id": "fergana", "name": "Fergana", "name_uz": "Farg'ona", "capital": "Fergana", "coordinates": [40.384, 71.789], "area_km2": 6800, "climate": "Continental, Fertile Valley", "avg_temperature": {"summer": 34, "winter": -3}, "annual_rainfall_mm": 180, "main_crops": ["Cotton", "Silk", "Rice", "Fruits", "Vegetables"], "soil_types": ["Alluvial", "Meadow"], "agricultural_area_hectares": 310000},
    {"id": "bukhara", "name": "Bukhara", "name_uz": "Buxoro", "capital": "Bukhara", "coordinates": [39.767, 64.421], "area_km2": 39400, "climate": "Arid, Desert", "avg_temperature": {"summer": 40, "winter": 1}, "annual_rainfall_mm": 140, "main_crops": ["Cotton", "Karakul Sheep", "Silkworm", "Wheat"], "soil_types": ["Sandy", "Desert Sierozem"], "agricultural_area_hectares": 280000},
    {"id": "andijan", "name": "Andijan", "name_uz": "Andijon", "capital": "Andijan", "coordinates": [40.783, 72.344], "area_km2": 4200, "climate": "Subtropical, Continental", "avg_temperature": {"summer": 35, "winter": -3}, "annual_rainfall_mm": 250, "main_crops": ["Cotton", "Wheat", "Silk", "Peaches", "Cherries"], "soil_types": ["Sierozem", "Alluvial"], "agricultural_area_hectares": 290000},
    {"id": "namangan", "name": "Namangan", "name_uz": "Namangan", "capital": "Namangan", "coordinates": [40.995, 71.672], "area_km2": 7900, "climate": "Continental", "avg_temperature": {"summer": 35, "winter": -2}, "annual_rainfall_mm": 230, "main_crops": ["Cotton", "Silk", "Flowers", "Apricots", "Apples"], "soil_types": ["Sierozem", "Stony Loam"], "agricultural_area_hectares": 270000},
    {"id": "jizzakh", "name": "Jizzakh", "name_uz": "Jizzax", "capital": "Jizzakh", "coordinates": [40.115, 67.842], "area_km2": 20500, "climate": "Extreme Continental", "avg_temperature": {"summer": 38, "winter": -4}, "annual_rainfall_mm": 320, "main_crops": ["Cotton", "Wheat", "Melons", "Grapes"], "soil_types": ["Sierozem", "Desert Clay"], "agricultural_area_hectares": 410000},
    {"id": "syrdarya", "name": "Syrdarya", "name_uz": "Sirdaryo", "capital": "Gulistan", "coordinates": [40.486, 68.715], "area_km2": 5100, "climate": "Continental", "avg_temperature": {"summer": 37, "winter": -2}, "annual_rainfall_mm": 280, "main_crops": ["Cotton", "Melons", "Rice", "Wheat"], "soil_types": ["Saline Meadow", "Sierozem"], "agricultural_area_hectares": 260000},
    {"id": "kashkadarya", "name": "Kashkadarya", "name_uz": "Qashqadaryo", "capital": "Karshi", "coordinates": [38.860, 65.800], "area_km2": 28400, "climate": "Arid, Dry Continental", "avg_temperature": {"summer": 39, "winter": 0}, "annual_rainfall_mm": 290, "main_crops": ["Cotton", "Wheat", "Cereals", "Sheep Breeding"], "soil_types": ["Sierozem", "Sandy Loam"], "agricultural_area_hectares": 580000},
    {"id": "surkhandarya", "name": "Surkhandarya", "name_uz": "Surxondaryo", "capital": "Termez", "coordinates": [37.224, 67.278], "area_km2": 20800, "climate": "Subtropical Dry", "avg_temperature": {"summer": 43, "winter": 3}, "annual_rainfall_mm": 200, "main_crops": ["Cotton", "Wheat", "Pomegranates", "Persimmons", "Figs"], "soil_types": ["Sierozem", "Takir"], "agricultural_area_hectares": 380000},
    {"id": "navoi", "name": "Navoi", "name_uz": "Navoiy", "capital": "Navoi", "coordinates": [40.103, 65.379], "area_km2": 111000, "climate": "Extreme Arid Desert", "avg_temperature": {"summer": 41, "winter": -4}, "annual_rainfall_mm": 120, "main_crops": ["Wheat", "Cotton", "Grapes", "Astrakhan Fur"], "soil_types": ["Desert Sandy", "Saline"], "agricultural_area_hectares": 320000},
    {"id": "khorezm", "name": "Khorezm", "name_uz": "Xorazm", "capital": "Urgench", "coordinates": [41.551, 60.631], "area_km2": 6300, "climate": "Arid Continental", "avg_temperature": {"summer": 37, "winter": -5}, "annual_rainfall_mm": 100, "main_crops": ["Cotton", "Wheat", "Rice", "Melons"], "soil_types": ["Alluvial Saline Meadow"], "agricultural_area_hectares": 210000},
    {"id": "karakalpakstan", "name": "Karakalpakstan", "name_uz": "Qoraqalpog'iston", "capital": "Nukus", "coordinates": [42.461, 59.606], "area_km2": 166600, "climate": "Extreme Arid", "avg_temperature": {"summer": 39, "winter": -8}, "annual_rainfall_mm": 90, "main_crops": ["Cotton", "Wheat", "Rice", "Melons", "Licorice"], "soil_types": ["Desert Saline", "Sands"], "agricultural_area_hectares": 450000},
]


class RegionsResponse(BaseModel):
    success: bool
    data: list


class RegionDetailResponse(BaseModel):
    success: bool
    data: dict


@router.get("/", response_model=RegionsResponse)
async def list_regions():
    """List all Uzbekistan regions with agricultural data."""
    return RegionsResponse(success=True, data=REGIONS)


@router.get("/{region_id}", response_model=RegionDetailResponse)
async def get_region(region_id: str):
    """Get detailed information for a specific region."""
    region = next((r for r in REGIONS if r["id"] == region_id), None)
    if not region:
        return RegionDetailResponse(success=False, data={"error": "Region not found"})
    return RegionDetailResponse(success=True, data=region)
