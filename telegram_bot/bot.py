"""
AgroVision AI — Telegram Bot
Asosiy kirish nuqtasi
"""

import os
import sys
import logging

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

    logger.info("🌿 AgroVision AI Bot ishga tushmoqda...")

    app = (
        Application.builder()
        .token(token)
        .post_init(post_init)
        .build()
    )

    # ── Handlerlarni ro'yxatga olish ──────────────────────────────────────
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("language", language_handler))
    app.add_handler(CommandHandler("about", about_handler))

    # Rasm handleri
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))

    # Inline keyboard callbacklar
    app.add_handler(CallbackQueryHandler(callback_handler))

    # Boshqa matnlarga javob
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            _text_fallback,
        )
    )

    logger.info("✅ Bot tayyor! Polling boshlanyapti...")
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )


async def _text_fallback(update, context) -> None:
    """Matn xabarga javob — rasm yuborishni so'raydi."""
    from services.user_store import get_lang
    from i18n.messages import get_msg
    from services.keyboards import main_keyboard
    from telegram.constants import ParseMode

    lang = get_lang(update.effective_user.id)
    web_url = os.getenv("WEB_APP_URL", "http://localhost:3001")
    await update.message.reply_text(
        get_msg(lang, "send_photo") + "\n\n" + get_msg(lang, "help"),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_keyboard(lang, web_url),
    )


if __name__ == "__main__":
    main()
