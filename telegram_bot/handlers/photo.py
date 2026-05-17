"""Rasm tahlil handleri — foydalanuvchi rasm yuborganda."""

import os
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from i18n.messages import get_msg
from services.user_store import get_lang, set_pending_photo
from services.keyboards import analysis_keyboard

WEB_APP_URL = os.getenv("WEB_APP_URL", "https://agro-vision-ai-zeta.vercel.app/")


async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Foydalanuvchi rasm yuborganda chaqiriladi."""
    user_id = update.effective_user.id
    lang = get_lang(user_id)

    # Eng yaxshi sifatli rasmni olamiz
    photo = update.message.photo[-1]
    photo_file = await context.bot.get_file(photo.file_id)
    photo_bytes = await photo_file.download_as_bytearray()

    # Rasmni xotirada saqlaymiz (callback kelguncha)
    set_pending_photo(user_id, bytes(photo_bytes))

    # Tahlil turini so'raymiz
    await update.message.reply_text(
        get_msg(lang, "choose_analysis"),
        reply_markup=analysis_keyboard(lang),
    )
