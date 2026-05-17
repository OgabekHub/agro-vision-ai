from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="AI-powered smart agriculture platform for Uzbekistan",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(api_router, prefix="/api/v1")

    @app.get("/", tags=["Health"])
    async def root():
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "status": "operational",
            "message": "AgroVision AI API is running 🌱",
        }

    @app.get("/health", tags=["Health"])
    async def health_check():
        import os
        gemini_key = os.environ.get("GEMINI_API_KEY", "")
        return {
            "status": "healthy",
            "gemini_api_key_status": {
                "exists": gemini_key != "",
                "length": len(gemini_key),
                "prefix": gemini_key[:4] if gemini_key else "None",
            },
            "models": {
                "yolov8": "loaded" if settings.DEBUG else "checking...",
                "efficientnet": "loaded" if settings.DEBUG else "checking...",
            },
        }

    return app


app = create_app()
