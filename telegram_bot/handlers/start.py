"""/start, /help, /language, /about handlerlari."""

import os
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from telegram.error import TimedOut, NetworkError

from i18n.messages import get_msg
from services.user_store import get_lang, set_lang
from services.keyboards import main_keyboard, language_keyboard

WEB_APP_URL = os.getenv("WEB_APP_URL", "https://agro-vision-ai-zeta.vercel.app/")


async def _send_with_retry(coro, retries: int = 3, delay: float = 2.0):
    """Telegram API timeout bo'lsa qayta urinib ko'radi."""
    last_exc = None
    for attempt in range(retries):
        try:
            return await coro
        except (TimedOut, NetworkError) as e:
            last_exc = e
            if attempt < retries - 1:
                await asyncio.sleep(delay * (attempt + 1))
    raise last_exc


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/start — Xush kelibsiz xabari va til tanlash."""
    user = update.effective_user
    user_id = user.id
    lang = get_lang(user_id)

    # Agar foydalanuvchi Telegram til sozlamasi bo'lsa, avtomatik o'rnatamiz
    tg_lang = user.language_code or ""
    if not lang or lang == "uz":
        if tg_lang.startswith("ru"):
            set_lang(user_id, "ru")
            lang = "ru"
        elif tg_lang.startswith("en"):
            set_lang(user_id, "en")
            lang = "en"

    # Til tanlash birinchi ko'rsatiladi
    await _send_with_retry(
        update.message.reply_text(
            get_msg(lang, "choose_language"),
            reply_markup=language_keyboard(),
        )
    )


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/help komandasi."""
    lang = get_lang(update.effective_user.id)
    await _send_with_retry(
        update.message.reply_text(
            get_msg(lang, "help"),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=main_keyboard(lang, WEB_APP_URL),
        )
    )


async def language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/language komandasi — til o'zgartirish."""
    lang = get_lang(update.effective_user.id)
    await _send_with_retry(
        update.message.reply_text(
            get_msg(lang, "choose_language"),
            reply_markup=language_keyboard(),
        )
    )


async def about_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/about komandasi."""
    lang = get_lang(update.effective_user.id)
    await _send_with_retry(
        update.message.reply_text(
            get_msg(lang, "about", web_url=WEB_APP_URL),
            parse_mode=ParseMode.MARKDOWN,
        )
    )
