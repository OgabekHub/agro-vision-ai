"""/start, /help, /language, /about handlerlari."""

import os
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from i18n.messages import get_msg
from services.user_store import get_lang, set_lang
from services.keyboards import main_keyboard, language_keyboard

WEB_APP_URL = os.getenv("WEB_APP_URL", "http://localhost:3001")


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
    await update.message.reply_text(
        get_msg(lang, "choose_language"),
        reply_markup=language_keyboard(),
    )


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/help komandasi."""
    lang = get_lang(update.effective_user.id)
    await update.message.reply_text(
        get_msg(lang, "help"),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_keyboard(lang, WEB_APP_URL),
    )


async def language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/language komandasi — til o'zgartirish."""
    lang = get_lang(update.effective_user.id)
    await update.message.reply_text(
        get_msg(lang, "choose_language"),
        reply_markup=language_keyboard(),
    )


async def about_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/about komandasi."""
    lang = get_lang(update.effective_user.id)
    await update.message.reply_text(
        get_msg(lang, "about", web_url=WEB_APP_URL),
        parse_mode=ParseMode.MARKDOWN,
    )
