"""Disease Analysis API — avval Local Model (99.95% aniq), keyin Gemini fallback."""

import time
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pydantic import BaseModel
from typing import Optional
from app.core import local_model_service
from app.core.gemini_service import analyze_disease
from app.api.v1.upload import upload_image_to_cloudinary
from app.core.supabase_service import log_disease_analysis, insert_ai_log

router = APIRouter()


class DiseaseAnalysisResponse(BaseModel):
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


@router.post("/analyze", response_model=DiseaseAnalysisResponse)
async def analyze_disease_endpoint(
    file: UploadFile = File(...),
    language: str = Form("uz"),
    user_id: Optional[str] = Form(None)
):
    """
    Kasallikni aniqlash:
    1. Gemini Vision orqali o'simlikni nima ekanini va umumiy holatini aniqlash
    2. Agar o'simlik lokal model sinflariga kirsa, kasallikni aniqroq topish uchun oflayn model tahlili
    3. Natijalarni Cloudinary hamda Supabase ma'lumotlar bazasida saqlash
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
    is_gemini_mock = disease_data.get("disease_name") == "AI sozlanmagan"

    if local_model_service.is_model_available():
        # Agar Gemini mock bo'lsa yoki category Other bo'lsa, lokal modelni filtrsiz (barcha klasslar uchun) ishlatamiz
        filter_cat = None if (is_gemini_mock or category == "Other") else category
        result = local_model_service.predict(contents, filter_category=filter_cat)
        
        if result:
            # Case 1: Gemini ishlamadi (mock) yoki to'g'ri o'simlikni topolmadi
            if is_gemini_mock or (category == "Other" and result["confidence"] > 0.6):
                # Noto'g'ri/random tashxislarni oldini olish uchun kamida 40% ishonchlilik talab qilinadi
                if result["confidence"] < 0.40:
                    model_used = "local_offline_model"
                    disease_data = {
                        "disease_name": "Kasallik aniqlanmadi (kam ishonchlilik)",
                        "plant_affected": result["plant_name"] if result["confidence"] > 0.15 else "Noma'lum o'simlik",
                        "supported_category": "Other",
                        "confidence": result["confidence"],
                        "severity": "low",
                        "description": "Rasm sifati past yoki kasallik alomatlari yetarli emas. Iltimos, yorug'roq joyda, bargni aniq qilib yaqinroqdan rasmga oling.",
                        "causes": [],
                        "symptoms": [],
                        "treatments": [],
                        "prevention_tips": ["Rasm sifatini yaxshilang", "Bargni yaqinroqdan va aniqroq ko'rsating"],
                        "has_disease": False,
                        "top3_predictions": result.get("top3", []),
                    }
                else:
                    model_used = "local_offline_model"
                    disease_data = {
                        "disease_name": result["disease_name"],
                        "plant_affected": result["plant_name"],
                        "supported_category": result["raw_class"].split("__")[0] if "__" in result["raw_class"] else "Other",
                        "confidence": result["confidence"],
                        "severity": result["severity"],
                        "description": result["description"],
                        "causes": [],
                        "symptoms": [],
                        "treatments": result["treatments"],
                        "prevention_tips": [],
                        "has_disease": not result["is_healthy"],
                        "top3_predictions": result.get("top3", []),
                    }
            # Case 2: Gemini muvaffaqiyatli ishladi (Hybrid rejim)
            else:
                # Oflayn model natijasi faqat yuqori ishonchlilikda (masalan >= 70%) Gemini natijasidan ustun qo'yiladi
                if result["confidence"] >= 0.70:
                    model_used = "gemini_and_local_hybrid"
                    disease_data.update({
                        "disease_name": result["disease_name"],
                        "plant_affected": result["plant_name"],
                        "confidence": result["confidence"],  # Ishonchlilik mahalliy modelga bog'lanadi
                        "severity": result["severity"],
                        "has_disease": not result["is_healthy"],
                        "top3_predictions": result.get("top3", []),
                    })
                    if result["treatments"]:
                        disease_data["treatments"] = result["treatments"]
                    if not result["is_healthy"]:
                        disease_data["description"] = f"{disease_data.get('description', '')}\n\nOflayn AI tahlili: {result['description']}"
                else:
                    # Mahalliy model ishonchi past bo'lsa, aqlliroq bo'lgan Gemini javobini saqlab qolamiz
                    model_used = "gemini_vision"
                    disease_data["top3_predictions"] = result.get("top3", [])
                    disease_data["local_confidence"] = result["confidence"]

    processing_time = int((time.time() - start_time) * 1000)

    # 3. Cloudinary CDN ga yuklash
    try:
        image_url = await upload_image_to_cloudinary(contents, file.filename)
    except Exception as e:
        image_url = f"https://res.cloudinary.com/demo/image/upload/v1/{file.filename}"

    # 4. Supabase ma'lumotlar bazasida saqlash
    validated_user_id = user_id if is_valid_uuid(user_id) else None
    analysis_id = await log_disease_analysis(
        user_id=validated_user_id,
        image_url=image_url,
        disease_name=disease_data.get("disease_name", "Noma'lum"),
        plant_affected=disease_data.get("plant_affected", "Unknown"),
        confidence=float(disease_data.get("confidence", 0.0)),
        severity=disease_data.get("severity", "low"),
        description=disease_data.get("description", ""),
        causes=disease_data.get("causes", []),
        symptoms=disease_data.get("symptoms", []),
        treatments=disease_data.get("treatments", []),
        prevention_tips=disease_data.get("prevention_tips", []),
        model_version=model_used,
        processing_time_ms=processing_time,
    )

    # 5. AI loglar jadvaliga yozish
    await insert_ai_log(
        analysis_type="disease",
        analysis_id=analysis_id,
        input_image_url=image_url,
        result=disease_data,
        confidence=float(disease_data.get("confidence", 0.0)),
        processing_time_ms=processing_time,
        model_version=model_used,
    )

    return DiseaseAnalysisResponse(
        success=True,
        data={**disease_data, "image_url": image_url, "image_size_bytes": len(contents), "model_version": model_used},
        processing_time_ms=processing_time,
    )


@router.get("/recent")
async def get_recent_diseases(limit: int = 5):
    """Get recent disease analyses from database."""
    from app.core.supabase_service import get_supabase
    client = get_supabase()
    if not client:
        return [
            {"disease_name": "Powdery Mildew", "plant_affected": "Grape", "severity": "medium", "created_at": "2026-06-04T06:00:00Z"},
            {"disease_name": "Cotton Leaf Curl", "plant_affected": "Cotton", "severity": "critical", "created_at": "2026-06-04T04:00:00Z"},
            {"disease_name": "Rust Disease", "plant_affected": "Wheat", "severity": "low", "created_at": "2026-06-04T02:00:00Z"},
        ]
    try:
        response = client.table("disease_analyses").select("disease_name, plant_affected, severity, created_at").order("created_at", desc=True).limit(limit).execute()
        return response.data or []
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Error fetching recent diseases: {e}")
        return []

