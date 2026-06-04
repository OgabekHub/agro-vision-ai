from fastapi import APIRouter
from app.api.v1 import plant, disease, recommend, weather, regions, admin, upload, auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(plant.router, prefix="/plant", tags=["Plant Detection"])
api_router.include_router(disease.router, prefix="/disease", tags=["Disease Analysis"])
api_router.include_router(recommend.router, prefix="/recommend", tags=["Recommendations"])
api_router.include_router(weather.router, prefix="/weather", tags=["Weather"])
api_router.include_router(regions.router, prefix="/regions", tags=["Regions"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
api_router.include_router(upload.router, prefix="/upload", tags=["Upload"])
