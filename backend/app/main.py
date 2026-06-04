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
        import subprocess
        
        gemini_env = os.environ.get("GEMINI_API_KEY", "")
        gemini_setting = settings.GEMINI_API_KEY
        
        bot_token_env = os.environ.get("TELEGRAM_BOT_TOKEN", "")
        
        # Check if bot.py process is running
        bot_running = False
        bot_pid = None
        try:
            # We can use pgrep to check for processes running bot.py
            result = subprocess.run(["pgrep", "-f", "bot.py"], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                bot_running = True
                bot_pid = result.stdout.strip().replace("\n", ", ")
        except Exception as e:
            # Fallback to checking via ps if pgrep is not available
            try:
                result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
                if "bot.py" in result.stdout:
                    bot_running = True
            except Exception:
                pass
                
        # Read bot logs
        bot_logs = ""
        try:
            log_paths = ["/code/bot.log", "bot.log", "telegram_bot/bot.log"]
            for path in log_paths:
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                        bot_logs = "".join(lines[-50:])
                    break
        except Exception as e:
            bot_logs = f"Error reading logs: {str(e)}"
            
        # Check network access to Telegram and Google
        telegram_api_ok = False
        telegram_api_err = None
        google_ok = False
        google_err = None
        try:
            import urllib.request
            urllib.request.urlopen("https://api.telegram.org", timeout=5)
            telegram_api_ok = True
        except Exception as e:
            telegram_api_err = str(e)
            
        try:
            import urllib.request
            urllib.request.urlopen("https://google.com", timeout=5)
            google_ok = True
        except Exception as e:
            google_err = str(e)
            
        proxy_org_ok = False
        proxy_org_err = None
        try:
            import urllib.request
            urllib.request.urlopen("https://api.telegram-proxy.org", timeout=5)
            proxy_org_ok = True
        except Exception as e:
            proxy_org_err = str(e)
            
        proxy_uz_ok = False
        proxy_uz_err = None
        try:
            import urllib.request
            urllib.request.urlopen("https://api.telegram.org.uz", timeout=5)
            proxy_uz_ok = True
        except Exception as e:
            proxy_uz_err = str(e)
            
        return {
            "status": "healthy",
            "gemini_api_key_status": {
                "env_exists": gemini_env != "",
                "env_length": len(gemini_env),
                "env_prefix": gemini_env[:4] if gemini_env else "None",
                "setting_exists": gemini_setting != "",
                "setting_length": len(gemini_setting),
                "setting_prefix": gemini_setting[:4] if gemini_setting else "None",
            },
            "telegram_bot_status": {
                "token_exists": bot_token_env != "",
                "token_length": len(bot_token_env),
                "token_prefix": bot_token_env[:9] if bot_token_env else "None",
                "process_running": bot_running,
                "process_pids": bot_pid,
                "api_accessible": telegram_api_ok,
                "api_error": telegram_api_err,
                "google_accessible": google_ok,
                "google_error": google_err,
                "proxy_org_accessible": proxy_org_ok,
                "proxy_org_error": proxy_org_err,
                "proxy_uz_accessible": proxy_uz_ok,
                "proxy_uz_error": proxy_uz_err,
                "logs": bot_logs,
            },
            "models": {
                "yolov8": "loaded",
                "efficientnet": "loaded",
            },
        }

    @app.get("/test-gemini-key", tags=["Debug"])
    async def test_gemini_key():
        import httpx
        key = settings.GEMINI_API_KEY
        if not key:
            return {"status": "error", "message": "GEMINI_API_KEY setting is empty"}
            
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}"
        payload = {
            "contents": [{"parts": [{"text": "Say test"}]}]
        }
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(url, json=payload)
                return {
                    "status": "completed",
                    "http_status": resp.status_code,
                    "response_text": resp.text[:1000],
                    "headers": dict(resp.headers),
                }
        except Exception as e:
            return {
                "status": "exception",
                "error_type": type(e).__name__,
                "error_msg": str(e),
            }

    return app


app = create_app()
