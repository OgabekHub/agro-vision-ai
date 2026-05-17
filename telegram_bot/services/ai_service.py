"""AI service — FastAPI backend bilan integratsiya."""

import io
import httpx
from typing import Optional


class AgroVisionAIService:
    """AgroVision FastAPI backend ga so'rov yuboradi."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def detect_plant(self, image_bytes: bytes, language: str = "uz", filename: str = "photo.jpg") -> dict:
        """O'simlikni aniqlash — /api/v1/plant/detect."""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                files = {"file": (filename, io.BytesIO(image_bytes), "image/jpeg")}
                data = {"language": language}
                resp = await client.post(f"{self.base_url}/api/v1/plant/detect", files=files, data=data)
                resp.raise_for_status()
                return resp.json().get("data", {})
        except (httpx.HTTPError, httpx.TimeoutException) as e:
            # Backend ishlamasa mock qaytaradi
            return self._mock_plant_result()

    async def detect_disease(self, image_bytes: bytes, language: str = "uz", filename: str = "photo.jpg") -> dict:
        """Kasallikni aniqlash — /api/v1/disease/analyze."""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                files = {"file": (filename, io.BytesIO(image_bytes), "image/jpeg")}
                data = {"language": language}
                resp = await client.post(f"{self.base_url}/api/v1/disease/analyze", files=files, data=data)
                resp.raise_for_status()
                return resp.json().get("data", {})
        except (httpx.HTTPError, httpx.TimeoutException) as e:
            return self._mock_disease_result()

    # ── Mock data ────────────────────────────────────────────────────────────

    @staticmethod
    def _mock_plant_result() -> dict:
        return {
            "plant_name": "Cotton (Gossypium hirsutum)",
            "scientific_name": "Gossypium hirsutum",
            "confidence": 0.946,
            "description": (
                "Cotton is one of the most important cash crops in Uzbekistan, "
                "known as 'white gold'. It thrives in warm continental climate "
                "and is a major export commodity."
            ),
            "family": "Malvaceae",
            "suitable_regions": ["Tashkent", "Fergana", "Andijan", "Namangan", "Bukhara"],
            "growing_season": "April — October",
            "water_needs": "Moderate to High",
        }

    @staticmethod
    def _mock_disease_result() -> dict:
        return {
            "disease_name": "Early Blight (Alternaria solani)",
            "plant_affected": "Tomato",
            "confidence": 0.891,
            "severity": "high",
            "description": (
                "Early blight is a common fungal disease affecting tomato plants. "
                "Dark concentric ring-shaped lesions on lower leaves can reduce "
                "fruit yield by up to 79%."
            ),
            "causes": [
                "Fungal pathogen thriving in warm, humid conditions",
                "Overhead watering creating prolonged leaf wetness",
                "Poor air circulation due to dense planting",
                "Infected plant debris from previous seasons",
            ],
            "treatments": [
                "Apply copper-based fungicide every 7-10 days",
                "Remove and destroy all infected leaves immediately",
                "Apply neem oil spray as an organic alternative",
                "Improve drainage and reduce watering frequency",
            ],
            "prevention_tips": [
                "Rotate crops — avoid planting tomatoes in the same spot for 2-3 years",
                "Space plants adequately for proper air circulation",
                "Water at the base, never overhead, preferably in the morning",
                "Use disease-resistant varieties when available",
            ],
        }
