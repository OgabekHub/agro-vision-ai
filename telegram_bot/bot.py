"""
AgroVision AI — Telegram Bot
Render.com Web Service uchun (bepul hosting):
- Telegram bot polling orqa fonda ishlaydi
- FastAPI health-check server old fonda ishlaydi (Render shart qo'yadi)
"""

import os
import sys
import logging
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# telegram_bot/ katalogini Python path ga qo'shamiz
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from handlers.start import start_handler, help_handler, language_handler, about_handler
from handlers.photo import photo_handler
from handlers.callbacks import callback_handler

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("agrovision_bot")


# ── Health-check HTTP server ───────────────────────────────────────────────────
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"AgroVision Bot is running!")

    def log_message(self, format, *args):
        pass  # HTTP loglarini o'chirish


def run_health_server():
    port = int(os.getenv("PORT", "10000"))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    logger.info(f"✅ Health server started on port {port}")
    server.serve_forever()


# ─────────────────────────────────────────────────────────────────────────────


async def post_init(application: Application) -> None:
    """Bot komandalarini Telegram da ro'yxatga olish."""
    commands = [
        BotCommand("start", "🌿 Botni boshlash / Запустить бота"),
        BotCommand("help", "📖 Yordam / Справка / Help"),
        BotCommand("language", "🌍 Tilni o'zgartirish / Язык / Language"),
        BotCommand("about", "ℹ️ Bot haqida / О боте / About"),
    ]
    await application.bot.set_my_commands(commands)
    logger.info("✅ Bot commands registered")


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("❌ TELEGRAM_BOT_TOKEN topilmadi! .env faylini tekshiring.")
        sys.exit(1)

    # Health-check serverni orqa fonda ishga tushirish (Render shart qiladi)
    health_thread = threading.Thread(target=run_health_server, daemon=True)
    health_thread.start()

    logger.info("🌿 AgroVision AI Bot ishga tushmoqda...")

    from telegram.request import HTTPXRequest
    request_config = HTTPXRequest(
        connect_timeout=60.0,
        read_timeout=60.0,
        write_timeout=60.0,
        pool_timeout=60.0,
    )

    builder = (
        Application.builder()
        .token(token)
        .request(request_config)
        .post_init(post_init)
    )

    # Custom API URL qo'llab-quvvatlash
    api_url = os.getenv("TELEGRAM_API_URL")
    if api_url:
        builder = builder.base_url(api_url)

    api_file_url = os.getenv("TELEGRAM_API_FILE_URL")
    if api_file_url:
        builder = builder.base_file_url(api_file_url)

    app = builder.build()

    # ── Handlerlarni ro'yxatga olish ──────────────────────────────────────
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("language", language_handler))
    app.add_handler(CommandHandler("about", about_handler))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, _text_fallback)
    )

    # ── Global xato handleri ───────────────────────────────────────────────
    app.add_error_handler(_error_handler)

    logger.info("✅ Bot tayyor! Polling boshlanyapdi...")
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
        bootstrap_retries=-1,
    )


async def _text_fallback(update, context) -> None:
    """Matn xabarga javob — rasm yuborishni so'raydi."""
    from services.user_store import get_lang
    from i18n.messages import get_msg
    from services.keyboards import main_keyboard
    from telegram.constants import ParseMode

    lang = get_lang(update.effective_user.id)
    web_url = os.getenv("WEB_APP_URL", "https://agro-vision-ai-zeta.vercel.app/")
    await update.message.reply_text(
        get_msg(lang, "send_photo") + "\n\n" + get_msg(lang, "help"),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_keyboard(lang, web_url),
    )


async def _error_handler(update: object, context) -> None:
    """Global xato handleri — tarmoq xatoliklarini tinchgina logga yozadi."""
    from telegram.error import TimedOut, NetworkError, BadRequest
    error = context.error
    if isinstance(error, TimedOut):
        logger.warning("⚠️ Telegram API timeout. Davom etilmoqda...")
        return
    if isinstance(error, NetworkError):
        logger.warning(f"⚠️ Tarmoq xatosi: {error}. Davom etilmoqda...")
        return
    if isinstance(error, BadRequest):
        logger.warning(f"⚠️ Bad Request: {error}")
        return
    logger.error(f"❌ Kutilmagan xato: {error}", exc_info=error)


if __name__ == "__main__":
    main()
