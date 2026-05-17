"""Plant Detection API — avval Local Model, keyin Gemini fallback."""

import time
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pydantic import BaseModel
from app.core import local_model_service
from app.core.gemini_service import analyze_plant

router = APIRouter()


class PlantDetectionResponse(BaseModel):
    success: bool
    data: dict
    processing_time_ms: int


@router.post("/detect", response_model=PlantDetectionResponse)
async def detect_plant(file: UploadFile = File(...), language: str = Form("uz")):
    """
    O'simlikni aniqlash:
    1. Gemini Vision orqali o'simlik turini aniq bilish (hamma o'simliklarni taniydi)
    2. Agar topilgan o'simlik lokal modelning 38 ta sinfiga kirsa, kasallikni oflayn modelda tekshirish (gibrid)
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
    return PlantDetectionResponse(
        success=True,
        data={**plant_data, "image_size_bytes": len(contents), "model_version": model_used},
        processing_time_ms=processing_time,
    )
