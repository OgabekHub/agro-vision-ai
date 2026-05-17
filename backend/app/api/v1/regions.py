"""Regions API endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

REGIONS = [
    {"id": "tashkent", "name": "Tashkent", "name_uz": "Toshkent", "capital": "Tashkent", "coordinates": [41.299, 69.240], "area_km2": 15300, "climate": "Continental, Semi-arid", "avg_temperature": {"summer": 36, "winter": -2}, "annual_rainfall_mm": 440, "main_crops": ["Cotton", "Wheat", "Vegetables", "Grapes", "Fruits"], "soil_types": ["Loamy", "Sierozem"], "agricultural_area_hectares": 420000},
    {"id": "samarkand", "name": "Samarkand", "name_uz": "Samarqand", "capital": "Samarkand", "coordinates": [39.654, 66.959], "area_km2": 16400, "climate": "Continental", "avg_temperature": {"summer": 35, "winter": -1}, "annual_rainfall_mm": 350, "main_crops": ["Cotton", "Wheat", "Silk", "Grapes", "Melons"], "soil_types": ["Sierozem", "Alluvial"], "agricultural_area_hectares": 510000},
    {"id": "fergana", "name": "Fergana", "name_uz": "Farg'ona", "capital": "Fergana", "coordinates": [40.384, 71.789], "area_km2": 6800, "climate": "Continental, Fertile Valley", "avg_temperature": {"summer": 34, "winter": -3}, "annual_rainfall_mm": 180, "main_crops": ["Cotton", "Silk", "Rice", "Fruits", "Vegetables"], "soil_types": ["Alluvial", "Meadow"], "agricultural_area_hectares": 310000},
    {"id": "bukhara", "name": "Bukhara", "name_uz": "Buxoro", "capital": "Bukhara", "coordinates": [39.767, 64.421], "area_km2": 39400, "climate": "Arid, Desert", "avg_temperature": {"summer": 40, "winter": 1}, "annual_rainfall_mm": 140, "main_crops": ["Cotton", "Karakul Sheep", "Silkworm", "Wheat"], "soil_types": ["Sandy", "Desert Sierozem"], "agricultural_area_hectares": 280000},
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
