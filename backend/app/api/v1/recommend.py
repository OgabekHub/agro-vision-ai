"""Crop Recommendation API endpoints."""

import time
import uuid
from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
from app.api.v1.upload import upload_image_to_cloudinary
from app.core.supabase_service import log_land_analysis, insert_ai_log

router = APIRouter()

SOIL_TYPES = [
    {
        "type": "Loamy Soil", "ph_level": 6.8, "moisture": "Moderate",
        "organic_matter": "Medium (3.2%)",
        "nutrients": {"nitrogen": "Adequate", "phosphorus": "Low", "potassium": "High"},
    },
    {
        "type": "Sandy Soil", "ph_level": 7.2, "moisture": "Low",
        "organic_matter": "Low (1.5%)",
        "nutrients": {"nitrogen": "Low", "phosphorus": "Adequate", "potassium": "Low"},
    },
    {
        "type": "Clay Soil", "ph_level": 6.5, "moisture": "High",
        "organic_matter": "High (4.8%)",
        "nutrients": {"nitrogen": "High", "phosphorus": "Adequate", "potassium": "Adequate"},
    },
]

CROP_RECOMMENDATIONS = [
    {"crop_name": "Cotton", "suitability_score": 0.94, "expected_yield": "3.2 tons/ha", "growing_period": "Apr-Oct", "irrigation_type": "Drip Irrigation", "tips": ["Plant after soil temp reaches 18°C", "Apply nitrogen at flowering stage"]},
    {"crop_name": "Wheat", "suitability_score": 0.88, "expected_yield": "4.5 tons/ha", "growing_period": "Oct-Jun", "irrigation_type": "Sprinkler", "tips": ["Ideal for winter planting", "Requires well-drained soil"]},
    {"crop_name": "Tomato", "suitability_score": 0.82, "expected_yield": "25 tons/ha", "growing_period": "Mar-Sep", "irrigation_type": "Drip Irrigation", "tips": ["Use raised beds", "Apply calcium for blossom end rot"]},
    {"crop_name": "Grape", "suitability_score": 0.79, "expected_yield": "8 tons/ha", "growing_period": "Mar-Oct", "irrigation_type": "Furrow", "tips": ["Excellent climate match", "Prune in late winter"]},
]


class RecommendationResponse(BaseModel):
    success: bool
    data: dict
    processing_time_ms: int


def is_valid_uuid(val: Optional[str]) -> bool:
    if not val:
        return False
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


@router.post("/crops", response_model=RecommendationResponse)
async def recommend_crops(
    file: UploadFile = File(...),
    region: Optional[str] = Form(None),
    language: str = Form("uz"),
    user_id: Optional[str] = Form(None)
):
    """Analyze land image and recommend optimal crops."""
    start_time = time.time()

    contents = await file.read()

    from app.core.gemini_service import analyze_land
    result = await analyze_land(contents, language=language)
    
    selected_region = region or "Tashkent"
    result["region"] = selected_region
    result["model_version"] = "Gemini-Pro-Vision"

    processing_time = int((time.time() - start_time) * 1000)

    # 3. Cloudinary CDN ga yuklash
    try:
        image_url = await upload_image_to_cloudinary(contents, file.filename)
    except Exception as e:
        image_url = f"https://res.cloudinary.com/demo/image/upload/v1/{file.filename}"

    # 4. Supabase ma'lumotlar bazasida saqlash
    validated_user_id = user_id if is_valid_uuid(user_id) else None
    analysis_id = await log_land_analysis(
        user_id=validated_user_id,
        image_url=image_url,
        soil_condition=result.get("soil_condition", {}),
        region=selected_region,
        recommended_crops=result.get("recommended_crops", []),
        farming_suggestions=result.get("farming_suggestions", []),
        irrigation_advice=result.get("irrigation_advice", ""),
        model_version=result["model_version"],
        processing_time_ms=processing_time,
    )

    # 5. AI loglar jadvaliga yozish
    await insert_ai_log(
        analysis_type="land",
        analysis_id=analysis_id,
        input_image_url=image_url,
        result=result,
        confidence=0.90,  # default confidence for Gemini land analysis
        processing_time_ms=processing_time,
        model_version=result["model_version"],
    )

    return RecommendationResponse(
        success=True,
        data={**result, "image_url": image_url},
        processing_time_ms=processing_time,
    )
