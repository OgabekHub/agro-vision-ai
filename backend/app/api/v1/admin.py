"""Admin API endpoints."""

import random
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class AdminStatsResponse(BaseModel):
    success: bool
    data: dict


class AdminLogsResponse(BaseModel):
    success: bool
    data: list
    total: int
    page: int


class AdminUsersResponse(BaseModel):
    success: bool
    data: list
    total: int


@router.get("/stats", response_model=AdminStatsResponse)
async def get_stats():
    """Get admin dashboard statistics."""
    return AdminStatsResponse(
        success=True,
        data={
            "total_analyses": 2847,
            "images_uploaded": 1932,
            "active_users": 456,
            "ai_accuracy": 94.7,
            "analyses_today": 47,
            "analyses_this_week": 312,
            "models": {
                "yolov8": {"status": "online", "version": "v8n-plant-v1", "total_inferences": 1245},
                "efficientnet": {"status": "online", "version": "B0-disease-v1", "total_inferences": 892},
                "opencv": {"status": "online", "version": "4.10", "total_inferences": 710},
            },
        },
    )


@router.get("/logs", response_model=AdminLogsResponse)
async def get_logs(page: int = 1, limit: int = 20):
    """Get AI analysis logs."""
    mock_logs = [
        {"id": str(i), "analysis_type": random.choice(["plant", "disease", "land"]),
         "result": random.choice(["Cotton detected", "Early Blight found", "Loamy soil analyzed", "Wheat detected", "Powdery Mildew"]),
         "confidence": round(random.uniform(0.75, 0.98), 3),
         "processing_time_ms": random.randint(150, 600),
         "model_version": random.choice(["YOLOv8n", "EfficientNet-B0", "OpenCV+ML"]),
         "created_at": f"2026-05-{random.randint(10, 16)}T{random.randint(8, 22):02d}:{random.randint(0, 59):02d}:00Z"}
        for i in range(limit)
    ]
    return AdminLogsResponse(success=True, data=mock_logs, total=2847, page=page)


@router.get("/users", response_model=AdminUsersResponse)
async def get_users(page: int = 1, limit: int = 20):
    """Get registered users."""
    users = [
        {"id": "1", "full_name": "Abdulaziz Karimov", "email": "abdulaziz@mail.uz", "role": "admin", "analyses_count": 156, "created_at": "2025-01-15"},
        {"id": "2", "full_name": "Nilufar Rashidova", "email": "nilufar@mail.uz", "role": "user", "analyses_count": 89, "created_at": "2025-03-22"},
        {"id": "3", "full_name": "Sardor Alimov", "email": "sardor@mail.uz", "role": "user", "analyses_count": 234, "created_at": "2025-02-10"},
        {"id": "4", "full_name": "Gulnora Yusupova", "email": "gulnora@mail.uz", "role": "user", "analyses_count": 67, "created_at": "2025-04-05"},
        {"id": "5", "full_name": "Jamshid Normatov", "email": "jamshid@mail.uz", "role": "user", "analyses_count": 112, "created_at": "2025-01-28"},
    ]
    return AdminUsersResponse(success=True, data=users, total=len(users))
