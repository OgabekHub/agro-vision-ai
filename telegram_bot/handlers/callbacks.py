"""Inline keyboard callback handlerlari (til tanlash, tahlil turi)."""

import os
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from i18n.messages import get_msg
from services.user_store import (
    get_lang, set_lang,
    get_pending_photo, clear_pending_photo,
)
from services.ai_service import AgroVisionAIService
from services.formatter import format_plant_result, format_disease_result
from services.keyboards import main_keyboard, result_keyboard

# API_BASE_URL — HF Spaces backend manzili
# PORT o'zgaruvchisiga qaramaymiz (Render uni health server uchun o'rnatadi)
API_BASE_URL = os.getenv("API_BASE_URL", "https://ogabekolimjonov-agro-vision-ai.hf.space")

WEB_APP_URL = os.getenv("WEB_APP_URL", "https://agro-vision-ai-zeta.vercel.app/")

ai_service = AgroVisionAIService(API_BASE_URL)


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Barcha inline keyboard callback larni boshqaradi."""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    data = query.data or ""

    # ── Til o'zgartirish ───────────────────────────────────────────────────
    if data.startswith("lang:"):
        new_lang = data.split(":")[1]
        set_lang(user_id, new_lang)
        lang = new_lang

        # Xush kelibsiz xabari
        await query.edit_message_text(
            get_msg(lang, "welcome"),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=main_keyboard(lang, WEB_APP_URL),
        )
        return

    # ── Til ko'rsatish ─────────────────────────────────────────────────────
    if data == "show:language":
        from services.keyboards import language_keyboard
        lang = get_lang(user_id)
        await query.edit_message_text(
            get_msg(lang, "choose_language"),
            reply_markup=language_keyboard(),
        )
        return

    # ── Tahlil turi tanlash ────────────────────────────────────────────────
    if data.startswith("analyze:"):
        lang = get_lang(user_id)
        analysis_type = data.split(":")[1]  # plant | disease | both

        photo_bytes = get_pending_photo(user_id)
        if not photo_bytes:
            await query.edit_message_text(get_msg(lang, "send_photo"))
            return

        # Loading xabari
        await query.edit_message_text(
            get_msg(lang, "analyzing"),
            parse_mode=ParseMode.MARKDOWN,
        )

        try:
            if analysis_type == "plant":
                result = await ai_service.detect_plant(photo_bytes, language=lang)
                text = format_plant_result(result, lang)
                await _send_result(query, text, lang)

            elif analysis_type == "disease":
                result = await ai_service.detect_disease(photo_bytes, language=lang)
                text = format_disease_result(result, lang)
                await _send_result(query, text, lang)

            elif analysis_type == "both":
                plant_task = asyncio.create_task(ai_service.detect_plant(photo_bytes, language=lang))
                disease_task = asyncio.create_task(ai_service.detect_disease(photo_bytes, language=lang))
                plant_result, disease_result = await asyncio.gather(plant_task, disease_task)

                plant_text = format_plant_result(plant_result, lang)
                disease_text = format_disease_result(disease_result, lang)

                await query.edit_message_text(
                    plant_text,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=result_keyboard(lang, WEB_APP_URL),
                )
                await query.message.reply_text(
                    disease_text,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=result_keyboard(lang, WEB_APP_URL),
                )

        except Exception:
            await query.edit_message_text(
                get_msg(lang, "error"),
                reply_markup=result_keyboard(lang, WEB_APP_URL),
            )
        finally:
            clear_pending_photo(user_id)


# ── Helpers ───────────────────────────────────────────────────────────────────

async def _send_result(query, text: str, lang: str) -> None:
    """Natijani inline keyboard bilan xabar sifatida yuboradi."""
    try:
        await query.edit_message_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=result_keyboard(lang, WEB_APP_URL),
        )
    except Exception:
        # Markdown xatosi bo'lsa, plain text
        await query.edit_message_text(
            text,
            reply_markup=result_keyboard(lang, WEB_APP_URL),
        )

