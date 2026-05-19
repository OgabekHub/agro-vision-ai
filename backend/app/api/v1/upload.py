"""Image Upload API endpoint with real Cloudinary integration."""

import asyncio
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import cloudinary
import cloudinary.uploader
from app.core.config import settings

router = APIRouter()

# Configure Cloudinary if keys are set
if settings.CLOUDINARY_CLOUD_NAME and settings.CLOUDINARY_API_KEY and settings.CLOUDINARY_API_SECRET:
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True
    )


class UploadResponse(BaseModel):
    success: bool
    data: dict


async def upload_image_to_cloudinary(contents: bytes, filename: str = "image.jpg") -> str:
    """Helper to upload image bytes and return URL. Falls back to mock URL if not configured."""
    if not (settings.CLOUDINARY_CLOUD_NAME and settings.CLOUDINARY_API_KEY and settings.CLOUDINARY_API_SECRET) or "your_api_key" in settings.CLOUDINARY_API_KEY:
        return f"https://res.cloudinary.com/demo/image/upload/v1/{filename}"

    loop = asyncio.get_event_loop()
    try:
        upload_result = await loop.run_in_executor(
            None,
            lambda: cloudinary.uploader.upload(
                contents,
                folder="agrovision",
                resource_type="auto"
            )
        )
        return upload_result.get("secure_url")
    except Exception as e:
        raise RuntimeError(f"Cloudinary upload failed: {e}")


@router.post("/image", response_model=UploadResponse)
async def upload_image(file: UploadFile = File(...)):
    """Upload image to Cloudinary CDN."""
    contents = await file.read()

    try:
        url = await upload_image_to_cloudinary(contents, file.filename)
        thumbnail_url = url.replace("/upload/", "/upload/c_thumb,w_200/") if "/upload/" in url else url
        return UploadResponse(
            success=True,
            data={
                "filename": file.filename,
                "size_bytes": len(contents),
                "content_type": file.content_type,
                "url": url,
                "thumbnail_url": thumbnail_url,
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
