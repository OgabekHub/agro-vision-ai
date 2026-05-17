"""Inline keyboard yordamchi funksiyalari."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from i18n.messages import get_msg

# Bot Telegram URL — doim ishlaydi (website deploy qilinguncha)
BOT_TELEGRAM_URL = "https://t.me/agro_visionai_bot"


def analysis_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Rasm tahlil turi tanlash klaviaturasi."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(get_msg(lang, "btn_plant"), callback_data="analyze:plant")],
        [InlineKeyboardButton(get_msg(lang, "btn_disease"), callback_data="analyze:disease")],
        [InlineKeyboardButton(get_msg(lang, "btn_both"), callback_data="analyze:both")],
    ])


def language_keyboard() -> InlineKeyboardMarkup:
    """Til tanlash klaviaturasi."""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇺🇿 O'zbek", callback_data="lang:uz"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang:ru"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang:en"),
        ]
    ])


def main_keyboard(lang: str, web_url: str) -> InlineKeyboardMarkup:
    """Asosiy menyudagi tugmalar.
    
    web_url https:// bo'lmasa, Bot Telegram havolasiga yo'naltiradi.
    """
    # Telegram faqat https:// URL qabul qiladi
    safe_url = web_url if web_url.startswith("https://") else BOT_TELEGRAM_URL

    return InlineKeyboardMarkup([
        [InlineKeyboardButton(get_msg(lang, "btn_web"), url=safe_url)],
        [InlineKeyboardButton(get_msg(lang, "btn_language"), callback_data="show:language")],
    ])


def result_keyboard(lang: str, web_url: str) -> InlineKeyboardMarkup:
    """Tahlil natijasi ostidagi tugmalar."""
    safe_url = web_url if web_url.startswith("https://") else BOT_TELEGRAM_URL
    new_photo_labels = {"uz": "📸 Yangi rasm", "ru": "📸 Новое фото", "en": "📸 New Photo"}
    new_label = new_photo_labels.get(lang, "📸 New Photo")

    return InlineKeyboardMarkup([
        [InlineKeyboardButton(new_label, callback_data="new:photo")],
        [InlineKeyboardButton(get_msg(lang, "btn_web"), url=safe_url)],
    ])
