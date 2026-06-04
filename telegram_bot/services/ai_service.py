"""AI service — FastAPI backend bilan integratsiya."""

import io
import logging
import httpx
from typing import Optional

logger = logging.getLogger(__name__)


class AgroVisionAIService:
    """AgroVision FastAPI backend ga so'rov yuboradi."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def detect_plant(self, image_bytes: bytes, language: str = "uz", filename: str = "photo.jpg") -> dict:
        """O'simlikni aniqlash — /api/v1/plant/detect."""
        logger.info(f"🌿 detect_plant → {self.base_url}/api/v1/plant/detect (lang={language}, size={len(image_bytes)}B)")
        try:
            async with httpx.AsyncClient(timeout=90.0) as client:
                files = {"file": (filename, io.BytesIO(image_bytes), "image/jpeg")}
                data = {"language": language}
                resp = await client.post(f"{self.base_url}/api/v1/plant/detect", files=files, data=data)
                resp.raise_for_status()
                result = resp.json().get("data", {})
                logger.info(f"✅ detect_plant natija: {result.get('plant_name', '?')} ({result.get('confidence', 0)*100:.1f}%)")
                return result
        except httpx.TimeoutException as e:
            logger.error(f"❌ detect_plant TIMEOUT (90s): {e}")
            return self._error_result("plant", f"Tahlil vaqti tugadi (90s). HF Spaces sekin javob berdi.")
        except httpx.HTTPStatusError as e:
            logger.error(f"❌ detect_plant HTTP {e.response.status_code}: {e.response.text[:200]}")
            return self._error_result("plant", f"Backend xatosi: {e.response.status_code}")
        except Exception as e:
            logger.error(f"❌ detect_plant xato: {type(e).__name__}: {e}")
            return self._error_result("plant", str(e))

    async def detect_disease(self, image_bytes: bytes, language: str = "uz", filename: str = "photo.jpg") -> dict:
        """Kasallikni aniqlash — /api/v1/disease/analyze."""
        logger.info(f"🦠 detect_disease → {self.base_url}/api/v1/disease/analyze (lang={language}, size={len(image_bytes)}B)")
        try:
            async with httpx.AsyncClient(timeout=90.0) as client:
                files = {"file": (filename, io.BytesIO(image_bytes), "image/jpeg")}
                data = {"language": language}
                resp = await client.post(f"{self.base_url}/api/v1/disease/analyze", files=files, data=data)
                resp.raise_for_status()
                result = resp.json().get("data", {})
                logger.info(f"✅ detect_disease natija: {result.get('disease_name', '?')} ({result.get('confidence', 0)*100:.1f}%)")
                return result
        except httpx.TimeoutException as e:
            logger.error(f"❌ detect_disease TIMEOUT (90s): {e}")
            return self._error_result("disease", "Tahlil vaqti tugadi (90s). HF Spaces sekin javob berdi.")
        except httpx.HTTPStatusError as e:
            logger.error(f"❌ detect_disease HTTP {e.response.status_code}: {e.response.text[:200]}")
            return self._error_result("disease", f"Backend xatosi: {e.response.status_code}")
        except Exception as e:
            logger.error(f"❌ detect_disease xato: {type(e).__name__}: {e}")
            return self._error_result("disease", str(e))

    # ── Xato natijalari ──────────────────────────────────────────────────────

    @staticmethod
    def _error_result(kind: str, reason: str) -> dict:
        """Xato bo'lganda foydalanuvchiga aniq xabar beradi (yashirin mock emas)."""
        if kind == "plant":
            return {
                "plant_name": "⚠️ Tahlil amalga oshmadi",
                "scientific_name": "—",
                "family": "—",
                "confidence": 0.0,
                "description": f"Xatolik: {reason}\n\nIltimos, qayta urinib ko'ring.",
                "growing_season": "—",
                "water_needs": "—",
                "suitable_regions": [],
                "is_plant": False,
                "_error": True,
            }
        else:
            return {
                "disease_name": "⚠️ Tahlil amalga oshmadi",
                "plant_affected": "—",
                "confidence": 0.0,
                "severity": "low",
                "description": f"Xatolik: {reason}\n\nIltimos, qayta urinib ko'ring.",
                "causes": [],
                "treatments": [],
                "prevention_tips": [],
                "has_disease": False,
                "_error": True,
            }
