"""Disease Analysis API — avval Local Model (99.95% aniq), keyin Gemini fallback."""

import time
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pydantic import BaseModel
from app.core import local_model_service
from app.core.gemini_service import analyze_disease

router = APIRouter()


class DiseaseAnalysisResponse(BaseModel):
    success: bool
    data: dict
    processing_time_ms: int


@router.post("/analyze", response_model=DiseaseAnalysisResponse)
async def analyze_disease_endpoint(file: UploadFile = File(...), language: str = Form("uz")):
    """
    Kasallikni aniqlash:
    1. Gemini Vision orqali o'simlikni nima ekanini va umumiy holatini aniqlash
    2. Agar o'simlik lokal model sinflariga kirsa, kasallikni aniqroq topish uchun oflayn model tahlili
    """
    start_time = time.time()

    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are accepted")

    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image too large (max 10MB)")

    # 1. Gemini orqali asosiy ma'lumotlarni olish
    model_used = "gemini_vision"
    disease_data = await analyze_disease(contents, language)

    # 2. Agar o'simlik bizning ro'yxatda bo'lsa, kasallikni Local Model bilan tahlil qilamiz
    category = disease_data.get("supported_category", "Other")

    if category != "Other" and local_model_service.is_model_available() and disease_data.get("has_disease") is not None:
        result = local_model_service.predict(contents, filter_category=category)
        if result:
            model_used = "gemini_and_local_hybrid"
            # Mahalliy modelning ishonchli va aniq javoblarini qo'shamiz
            disease_data.update({
                "disease_name": result["disease_name"],
                "plant_affected": result["plant_name"],
                "local_confidence": result["confidence"],
                "severity": result["severity"],
                "has_disease": not result["is_healthy"],
                "top3_predictions": result.get("top3", []),
            })
            
            # Agar lokal model davolash usullarini topsa, ularni ustun qo'yamiz
            if result["treatments"]:
                disease_data["treatments"] = result["treatments"]
            
            # Description'ga qo'shimcha kiritamiz
            if not result["is_healthy"]:
                disease_data["description"] = f"{disease_data.get('description', '')}\n\nOflayn AI tahlili: {result['description']}"

    processing_time = int((time.time() - start_time) * 1000)
    return DiseaseAnalysisResponse(
        success=True,
        data={**disease_data, "image_size_bytes": len(contents), "model_version": model_used},
        processing_time_ms=processing_time,
    )
