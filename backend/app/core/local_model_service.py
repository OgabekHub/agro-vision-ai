"""
Local EfficientNet-B3 inference — Gemini'siz, oflayn ishlaydi
109 ta kasallik/o'simlik turi/zararkunanda
"""

import os
import json
import io
import logging
from pathlib import Path
from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image

logger = logging.getLogger(__name__)

# Model yo'li
BASE = Path(__file__).parent.parent.parent / "models_weights"
MODEL_PATH = BASE / "mega_plant_disease_model.pth"
if not MODEL_PATH.exists():
    MODEL_PATH = BASE / "plant_disease_model.pth"
CLASSES_PATH = BASE / "class_names.json"

IMG_SIZE = 224
TRANSFORM = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])

# ── Sinf ma'lumotlari (tarjimalar) ───────────────────────────────────────
DISEASE_INFO = {}
TRANSLATIONS_PATH = BASE / "disease_translations.json"

def _load_translations():
    global DISEASE_INFO
    if TRANSLATIONS_PATH.exists():
        try:
            with open(TRANSLATIONS_PATH, "r", encoding="utf-8") as f:
                DISEASE_INFO = json.load(f)
        except Exception as e:
            logger.error(f"Tarjimalar yuklashda xato: {e}")
    else:
        logger.warning("disease_translations.json topilmadi. Asl nomlardan foydalaniladi.")

# ── Model yuklash ────────────────────────────────────────────────────────────
_model: Optional[nn.Module] = None
_classes: Optional[list] = None


def _load_model():
    global _model, _classes
    if _model is not None:
        return True
    if not MODEL_PATH.exists() or not CLASSES_PATH.exists():
        logger.warning(f"Model fayli topilmadi: {MODEL_PATH}")
        return False
    try:
        _load_translations()
        with open(CLASSES_PATH) as f:
            data = json.load(f)
        _classes = data.get("classes", data) # Support both dict format and pure list
        if isinstance(_classes, dict) and "classes" in _classes:
            _classes = _classes["classes"]
        num_classes = len(_classes)

        m = models.efficientnet_b3(weights=None)
        in_features = m.classifier[1].in_features
        m.classifier[1] = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(in_features, num_classes),
        )
        state = torch.load(MODEL_PATH, map_location="cpu", weights_only=True)
        m.load_state_dict(state)
        m.eval()
        _model = m
        logger.info(f"✅ Local model yuklandi: {num_classes} sinf, {MODEL_PATH.stat().st_size/1024/1024:.1f}MB")
        return True
    except Exception as e:
        logger.error(f"Model yuklashda xato: {e}")
        return False


def is_model_available() -> bool:
    return _load_model()


def predict(image_bytes: bytes, filter_category: Optional[str] = None) -> dict:
    """Rasmdan kasallik/o'simlik aniqlab qaytaradi.
    filter_category berilsa, faqat o'sha kategoriya uchun bashorat qiladi.
    """
    if not _load_model():
        return None

    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        tensor = TRANSFORM(img).unsqueeze(0)

        with torch.no_grad():
            logits = _model(tensor)
            probs = F.softmax(logits, dim=1)
            
            if filter_category and filter_category != "Other":
                for i, c in enumerate(_classes):
                    if not c.startswith(filter_category):
                        probs[0][i] = 0.0
                
                if probs.sum() > 0:
                    probs = probs / probs.sum()

            top_prob, top_idx = probs.topk(3, dim=1)

        top_class = _classes[top_idx[0][0].item()]
        confidence = top_prob[0][0].item()

        info = DISEASE_INFO.get(top_class, {})
        
        # Fallback values if the class isn't in translations yet
        # Support both '___' (old dataset) and '__' (new dataset) separators
        separator = "___" if "___" in top_class else "__" if "__" in top_class else None
        
        if separator:
            fallback_plant = top_class.split(separator)[0].replace("_", " ")
            fallback_disease = top_class.split(separator)[1].replace("_", " ") if len(top_class.split(separator)) > 1 else top_class
        else:
            fallback_plant = top_class
            fallback_disease = top_class
        
        plant_name = info.get("plant", fallback_plant)
        disease_name = info.get("disease", fallback_disease)
        is_healthy = "healthy" in top_class.lower()

        return {
            "raw_class": top_class,
            "plant_name": plant_name,
            "disease_name": disease_name,
            "confidence": round(confidence, 4),
            "severity": info.get("severity", "low" if is_healthy else "medium"),
            "description": info.get("description", f"Detected {disease_name} on {plant_name}."),
            "treatments": info.get("treatments", []),
            "is_healthy": is_healthy,
            "top3": [
                {"class": _classes[top_idx[0][i].item()], "prob": round(top_prob[0][i].item(), 4)}
                for i in range(3)
            ],
        }
    except Exception as e:
        logger.error(f"Prediction xato: {e}")
        return None
