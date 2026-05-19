"""Plant Detection API — avval Local Model, keyin Gemini fallback."""

import time
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pydantic import BaseModel
from typing import Optional
from app.core import local_model_service
from app.core.gemini_service import analyze_plant
from app.api.v1.upload import upload_image_to_cloudinary
from app.core.supabase_service import log_plant_analysis, insert_ai_log

router = APIRouter()


class PlantDetectionResponse(BaseModel):
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


@router.post("/detect", response_model=PlantDetectionResponse)
async def detect_plant(
    file: UploadFile = File(...),
    language: str = Form("uz"),
    user_id: Optional[str] = Form(None)
):
    """
    O'simlikni aniqlash:
    1. Gemini Vision orqali o'simlik turini aniq bilish (hamma o'simliklarni taniydi)
    2. Agar topilgan o'simlik lokal modelning 38 ta sinfiga kirsa, kasallikni oflayn modelda tekshirish (gibrid)
    3. Rasm va natijalarni Cloudinary hamda Supabase ma'lumotlar bazasida saqlash
    """
    start_time = time.time()

    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are accepted")

    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image too large (max 10MB)")

    # 1. Gemini orqali o'simlik nomini va ma'lumotlarini aniqlash
    model_used = "gemini_vision"
    plant_data = await analyze_plant(contents, language)

    # 2. Agar o'simlik bizning ro'yxatda bo'lsa (Apple, Tomato, etc.), kasallikni Local Model da ko'ramiz
    category = plant_data.get("supported_category", "Other")

    if category != "Other" and local_model_service.is_model_available() and plant_data.get("is_plant", False):
        # Lokal model faqatgina shu 'category' bo'yicha bashorat qiladi
        result = local_model_service.predict(contents, filter_category=category)
        if result:
            model_used = "gemini_and_local_hybrid"
            plant_data["disease_detected"] = result["disease_name"]
            plant_data["local_confidence"] = result["confidence"]
            plant_data["top3_predictions"] = result.get("top3", [])
            
            # Agar kasallik topsa, ta'rifiga qo'shib qo'yamiz
            if not result["is_healthy"]:
                disease_info = f"\n\n🩺 Diqqat: Ushbu o'simlikda kasallik aniqlandi: {result['disease_name']}."
                plant_data["description"] = plant_data.get("description", "") + disease_info

    processing_time = int((time.time() - start_time) * 1000)

    # 3. Cloudinary CDN ga yuklash
    try:
        image_url = await upload_image_to_cloudinary(contents, file.filename)
    except Exception as e:
        image_url = f"https://res.cloudinary.com/demo/image/upload/v1/{file.filename}"

    # 4. Supabase ma'lumotlar bazasida saqlash
    validated_user_id = user_id if is_valid_uuid(user_id) else None
    analysis_id = await log_plant_analysis(
        user_id=validated_user_id,
        image_url=image_url,
        plant_name=plant_data.get("plant_name", "Noma'lum"),
        scientific_name=plant_data.get("scientific_name", "Unknown"),
        family=plant_data.get("family", "Unknown"),
        confidence=float(plant_data.get("confidence", 0.0)),
        description=plant_data.get("description", ""),
        suitable_regions=plant_data.get("suitable_regions", []),
        growing_season=plant_data.get("growing_season", ""),
        water_needs=plant_data.get("water_needs", ""),
        model_version=model_used,
        processing_time_ms=processing_time,
    )

    # 5. AI loglar jadvaliga yozish
    await insert_ai_log(
        analysis_type="plant",
        analysis_id=analysis_id,
        input_image_url=image_url,
        result=plant_data,
        confidence=float(plant_data.get("confidence", 0.0)),
        processing_time_ms=processing_time,
        model_version=model_used,
    )

    return PlantDetectionResponse(
        success=True,
        data={**plant_data, "image_url": image_url, "image_size_bytes": len(contents), "model_version": model_used},
        processing_time_ms=processing_time,
    )
