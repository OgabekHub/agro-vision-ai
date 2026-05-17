"""Image Upload API endpoint."""

from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

router = APIRouter()


class UploadResponse(BaseModel):
    success: bool
    data: dict


@router.post("/image", response_model=UploadResponse)
async def upload_image(file: UploadFile = File(...)):
    """Upload image. In production, uploads to Cloudinary CDN."""
    contents = await file.read()
    file_size = len(contents)

    # In production: upload to Cloudinary
    # result = cloudinary.uploader.upload(contents, folder="agrovision")

    return UploadResponse(
        success=True,
        data={
            "filename": file.filename,
            "size_bytes": file_size,
            "content_type": file.content_type,
            "url": f"https://res.cloudinary.com/demo/image/upload/v1/{file.filename}",
            "thumbnail_url": f"https://res.cloudinary.com/demo/image/upload/c_thumb,w_200/{file.filename}",
        },
    )
