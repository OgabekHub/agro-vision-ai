"""
Gemini Vision AI Service — httpx REST API orqali (SDK muammosiz)
Rasmdan o'simlik va kasallikni aniqlik bilan tahlil qiladi.
"""

import os
import json
import re
import base64
import logging
import asyncio
from typing import Optional
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)

# Gemini REST API endpoint
GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
# Bepul limitlar eng ko'p bo'lgan model
GEMINI_MODEL = "gemini-2.5-flash"


def _get_api_key() -> Optional[str]:
    key = settings.GEMINI_API_KEY
    if not key or key == "your_gemini_api_key_here":
        return None
    return key


def _build_request(prompt: str, image_bytes: bytes) -> dict:
    """Gemini REST API uchun so'rov tanasini tayyorlaydi."""
    b64 = base64.b64encode(image_bytes).decode()
    return {
        "contents": [{
            "parts": [
                {"text": prompt},
                {"inlineData": {"mimeType": "image/jpeg", "data": b64}},
            ]
        }],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 1500,
        },
    }


def _parse_json(text: str) -> Optional[dict]:
    """AI javobidan JSON ob'ektini ajratib oladi."""
    # ```json ... ``` blok
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        text = match.group(1)
    else:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end > start:
            text = text[start:end]
    try:
        return json.loads(text)
    except Exception:
        return None


async def _call_gemini(prompt: str, image_bytes: bytes) -> Optional[str]:
    """Gemini REST API ga asinxron so'rov yuboradi."""
    api_key = _get_api_key()
    if not api_key:
        return None

    url = f"{GEMINI_API_BASE}/{GEMINI_MODEL}:generateContent?key={api_key}"
    payload = _build_request(prompt, image_bytes)

    # Bir necha model bilan sinab ko'ramiz (fallback)
    models_to_try = [GEMINI_MODEL, "gemini-2.0-flash-lite", "gemini-2.0-flash", "gemini-2.5-pro"]

    for model in models_to_try:
        try:
            url = f"{GEMINI_API_BASE}/{model}:generateContent?key={api_key}"
            async with httpx.AsyncClient(timeout=45.0) as client:
                resp = await client.post(url, json=payload)
                if resp.status_code == 429:
                    logger.warning(f"Model {model} quota exceeded, trying next...")
                    await asyncio.sleep(1)
                    continue
                resp.raise_for_status()
                data = resp.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                logger.info(f"✅ Gemini ({model}) javob berdi")
                return text
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                logger.warning(f"Model {model} rate limited")
                continue
            logger.error(f"HTTP error with {model}: {e}")
            continue
        except Exception as e:
            logger.error(f"Error with {model}: {e}")
            continue

    logger.error("Barcha Gemini modellari xato qaytardi")
    return None


# ── PLANT DETECTION ─────────────────────────────────────────────────────────

PLANT_PROMPT = """You are an expert agricultural botanist specializing in Central Asian and Uzbekistan plants.

Analyze this plant image carefully and identify the plant species.

Return ONLY a valid JSON object (no extra text) in this exact format:
{
  "plant_name": "Common name (Scientific name)",
  "scientific_name": "Genus species",
  "family": "Plant family name",
  "confidence": 0.92,
  "description": "2-3 sentences about this plant, mentioning its importance in Uzbekistan or Central Asia if relevant.",
  "growing_season": "Month — Month (e.g. April — October)",
  "water_needs": "Low / Moderate / High / Very High",
  "suitable_regions": ["Region1", "Region2"],
  "is_plant": true,
  "supported_category": "Apple"
}

For suitable_regions, choose from: Tashkent, Fergana, Andijan, Namangan, Samarkand, Bukhara, Kashkadarya, Surkhandarya, Jizzakh, Syrdarya, Khorezm, Karakalpakstan, Navoi.

If the image does NOT contain a plant, return:
{"is_plant": false, "plant_name": "No plant detected", "confidence": 0.0, "supported_category": "Other"}

confidence should reflect your actual certainty (0.0-1.0). Be precise and accurate.
CRITICAL: "supported_category" MUST be exactly one of: 'Apple', 'Cassava', 'Cherry', 'Chili', 'Coffee', 'Corn', 'Cotton', 'Cucumber', 'Gauva', 'Grape', 'Jamun', 'Lemon', 'Mango', 'Peach', 'Pepper_bell', 'Pest_Insect', 'Pomegranate', 'Potato', 'Rice', 'Soybean', 'Strawberry', 'Sugarcane', 'Tea', 'Tomato', 'Wheat', or 'Other' if it's none of these."""


DISEASE_PROMPT = """You are an expert plant pathologist specializing in agricultural diseases in Uzbekistan and Central Asia.

Analyze this plant/leaf/fruit image for diseases, pests, or nutrient deficiencies.

Return ONLY a valid JSON object (no extra text) in this exact format:
{
  "disease_name": "Disease common name (Pathogen name if known)",
  "plant_affected": "Plant species common name",
  "supported_category": "Apple",
  "confidence": 0.88,
  "severity": "low",
  "description": "2-3 sentences describing the disease and its impact on yield.",
  "causes": ["Specific cause 1", "Specific cause 2", "Specific cause 3"],
  "symptoms": ["Visible symptom 1", "Visible symptom 2", "Visible symptom 3"],
  "treatments": ["Specific treatment 1 with product type", "Treatment 2", "Treatment 3", "Treatment 4"],
  "prevention_tips": ["Prevention 1", "Prevention 2", "Prevention 3", "Prevention 4"],
  "has_disease": true
}

severity must be one of: "low", "medium", "high", "critical"

If the plant looks HEALTHY:
{
  "disease_name": "No disease detected",
  "plant_affected": "Healthy plant",
  "supported_category": "Apple",
  "confidence": 0.90,
  "severity": "low",
  "description": "The plant appears healthy with no visible signs of disease or pest damage.",
  "causes": [],
  "symptoms": ["No symptoms detected — plant looks healthy"],
  "treatments": ["No treatment needed — continue normal care"],
  "prevention_tips": ["Regular monitoring", "Proper watering schedule", "Good air circulation", "Balanced fertilization"],
  "has_disease": false
}

Be specific. Mention treatments suitable for small-scale farmers in Uzbekistan.
CRITICAL: "supported_category" MUST be exactly one of: 'Apple', 'Cassava', 'Cherry', 'Chili', 'Coffee', 'Corn', 'Cotton', 'Cucumber', 'Gauva', 'Grape', 'Jamun', 'Lemon', 'Mango', 'Peach', 'Pepper_bell', 'Pest_Insect', 'Pomegranate', 'Potato', 'Rice', 'Soybean', 'Strawberry', 'Sugarcane', 'Tea', 'Tomato', 'Wheat', or 'Other' if it's none of these."""


async def analyze_plant(image_bytes: bytes, language: str = "uz") -> dict:
    """Rasmdan o'simlikni aniqlab, batafsil ma'lumot qaytaradi."""
    lang_instruction = f"\n\nCRITICAL INSTRUCTION: You MUST translate ALL string values in the JSON (such as plant_name, family, description, water_needs) into the language corresponding to this code: '{language}' (e.g. if 'uz' or 'uz-UZ', use Uzbek; if 'ru', use Russian). NEVER use English unless the code is 'en'. Scientific names should remain in Latin."
    prompt = PLANT_PROMPT + lang_instruction
    text = await _call_gemini(prompt, image_bytes)

    if text is None:
        logger.warning("Gemini not available — returning mock")
        return _mock_plant()

    data = _parse_json(text)
    if data and data.get("is_plant", True):
        if not data.get("suitable_regions"):
            data["suitable_regions"] = ["Tashkent", "Fergana", "Samarkand"]
        return data
    elif data and not data.get("is_plant"):
        return {
            "plant_name": "O'simlik aniqlanmadi",
            "scientific_name": "Unknown",
            "family": "Unknown",
            "confidence": 0.1,
            "description": "Rasmda o'simlik aniq ko'rinmayapdi. Iltimos, o'simlik, barg yoki ekin rasmini yuklang.",
            "growing_season": "—",
            "water_needs": "—",
            "suitable_regions": [],
            "is_plant": False,
        }
    else:
        logger.error(f"JSON parse error. Raw: {text[:300]}")
        return _mock_plant()


async def analyze_disease(image_bytes: bytes, language: str = "uz") -> dict:
    """Rasmdan kasallikni aniqlab, davolash tavsiyalari qaytaradi."""
    lang_instruction = f"\n\nCRITICAL INSTRUCTION: You MUST translate ALL string values in the JSON (such as disease_name, description, causes, symptoms, treatments, prevention_tips) into the language corresponding to this code: '{language}' (e.g. if 'uz' or 'uz-UZ', use Uzbek; if 'ru', use Russian). NEVER use English unless the code is 'en'. Scientific names should remain in Latin."
    prompt = DISEASE_PROMPT + lang_instruction
    text = await _call_gemini(prompt, image_bytes)

    if text is None:
        logger.warning("Gemini not available — returning mock")
        return _mock_disease()

    data = _parse_json(text)
    if data:
        data.setdefault("causes", [])
        data.setdefault("symptoms", [])
        data.setdefault("treatments", [])
        data.setdefault("prevention_tips", [])
        data.setdefault("severity", "low")
        return data
    else:
        logger.error(f"JSON parse error. Raw: {text[:300]}")
        return _mock_disease()


# ── MOCK FALLBACKS ────────────────────────────────────────────────────────────

def _mock_plant() -> dict:
    return {
        "plant_name": "Cotton (Gossypium hirsutum)",
        "scientific_name": "Gossypium hirsutum",
        "family": "Malvaceae",
        "confidence": 0.50,
        "description": "⚠️ AI tahlil mavjud emas. GEMINI_API_KEY ni tekshiring yoki https://aistudio.google.com/app/apikey dan yangi key oling.",
        "growing_season": "April — October",
        "water_needs": "Moderate to High",
        "suitable_regions": ["Tashkent", "Fergana", "Andijan"],
        "is_plant": True,
    }


def _mock_disease() -> dict:
    return {
        "disease_name": "AI sozlanmagan",
        "plant_affected": "Noma'lum",
        "confidence": 0.50,
        "severity": "low",
        "description": "⚠️ Gemini API key ishlamayapdi. https://aistudio.google.com/app/apikey dan yangi key oling.",
        "causes": ["GEMINI_API_KEY noto'g'ri yoki limit tugagan"],
        "symptoms": ["Tahlil qilib bo'lmadi"],
        "treatments": ["AI Studio dan yangi key oling: https://aistudio.google.com/app/apikey"],
        "prevention_tips": ["Google accountingizga kiring", "AI Studio → API Keys → Create"],
        "has_disease": False,
    }

LAND_PROMPT = """You are an expert agricultural scientist specializing in Central Asian and Uzbekistan soil and agriculture.

Analyze this image of land/soil.

Return ONLY a valid JSON object (no extra text) in this exact format:
{
  "soil_condition": {
    "type": "Soil type (e.g. Loamy Soil, Sandy Soil, Clay Soil)",
    "ph_level": 6.8,
    "moisture": "Moderate",
    "organic_matter": "Medium (3.2%)",
    "nutrients": {
      "nitrogen": "Adequate",
      "phosphorus": "Low",
      "potassium": "High"
    }
  },
  "recommended_crops": [
    {
      "crop_name": "Wheat",
      "suitability_score": 0.88,
      "expected_yield": "4.5 tons/ha",
      "growing_period": "Oct-Jun",
      "irrigation_type": "Sprinkler",
      "tips": ["Tip 1", "Tip 2"]
    }
  ],
  "farming_suggestions": [
    "Suggestion 1", "Suggestion 2", "Suggestion 3"
  ],
  "irrigation_advice": "Detailed advice on irrigation for this land."
}
"""

async def analyze_land(image_bytes: bytes, language: str = "uz") -> dict:
    """Rasmdan yer va tuproqni tahlil qilib, ekin tavsiya qiladi."""
    lang_instruction = f"\n\nCRITICAL INSTRUCTION: You MUST translate ALL string values in the JSON (except the keys) into the language corresponding to this code: '{language}' (e.g. if 'uz' or 'uz-UZ', use Uzbek; if 'ru', use Russian). NEVER use English unless the code is 'en'."
    prompt = LAND_PROMPT + lang_instruction
    text = await _call_gemini(prompt, image_bytes)

    if text is None:
        logger.warning("Gemini not available — returning mock")
        return _mock_land()

    data = _parse_json(text)
    if data:
        return data
    else:
        logger.error(f"JSON parse error. Raw: {text[:300]}")
        return _mock_land()

def _mock_land() -> dict:
    return {
        "soil_condition": {
            "type": "Loamy Soil", "ph_level": 6.8, "moisture": "Moderate",
            "organic_matter": "Medium (3.2%)",
            "nutrients": {"nitrogen": "Adequate", "phosphorus": "Low", "potassium": "High"},
        },
        "recommended_crops": [
            {"crop_name": "Cotton", "suitability_score": 0.94, "expected_yield": "3.2 tons/ha", "growing_period": "Apr-Oct", "irrigation_type": "Drip Irrigation", "tips": ["Plant after soil temp reaches 18°C"]},
        ],
        "farming_suggestions": ["AI tahlil mavjud emas."],
        "irrigation_advice": "⚠️ Gemini API key ishlamayapdi."
    }
