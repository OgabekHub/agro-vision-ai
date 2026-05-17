"""
AgroVision AI — Telegram Bot
UZ / RU / EN ko'p tilli qo'llab-quvvatlash
"""

MESSAGES = {
    "uz": {
        "welcome": (
            "🌿 *AgroVision AI Botiga xush kelibsiz!*\n\n"
            "Bu bot sizga qishloq xo'jaligi sohasida AI yordamida:\n\n"
            "🔬 *O'simlikni aniqlash* — rasm yuboring\n"
            "🦠 *Kasallikni aniqlash* — barg/meva rasmi\n"
            "🌾 *Davolash tavsiyalari* — kasallik aniqlanganda\n\n"
            "📸 *Boshlash uchun rasm yuboring!*"
        ),
        "help": (
            "📖 *Yordam*\n\n"
            "1️⃣ Rasm yuboring (o'simlik yoki barg)\n"
            "2️⃣ Tahlil turini tanlang\n"
            "3️⃣ AI natijasini oling\n\n"
            "🌐 *Buyruqlar:*\n"
            "/start — Boshlanish\n"
            "/help — Yordam\n"
            "/language — Tilni o'zgartirish\n"
            "/about — Bot haqida"
        ),
        "choose_analysis": "📸 Rasm qabul qilindi! Tahlil turini tanlang:",
        "analyzing": "⏳ *Tahlil qilinmoqda...*\nAI model ishlamoqda, bir oz kuting.",
        "plant_result": (
            "🌿 *O'simlik aniqlandi!*\n\n"
            "📛 *Nomi:* {plant_name}\n"
            "🔬 *Ilmiy nomi:* _{scientific_name}_\n"
            "🏷️ *Oilasi:* {family}\n"
            "📊 *Ishonchlilik:* *{confidence}%*\n\n"
            "📝 *Ma'lumot:*\n{description}\n\n"
            "🌱 *O'sish mavsumi:* {growing_season}\n"
            "💧 *Suv ehtiyoji:* {water_needs}\n\n"
            "📍 *O'zbekistondagi mos viloyatlar:*\n{regions}"
        ),
        "disease_result": (
            "🦠 *Kasallik aniqlandi!*\n\n"
            "⚕️ *Kasallik:* {disease_name}\n"
            "🌿 *Ta'sir etuvchi o'simlik:* {plant_affected}\n"
            "🚨 *Og'irlik darajasi:* {severity}\n"
            "📊 *Ishonchlilik:* *{confidence}%*\n\n"
            "📝 *Tavsif:*\n{description}\n\n"
            "⚠️ *Sabablar:*\n{causes}\n\n"
            "💊 *Davolash tavsiyalari:*\n{treatments}\n\n"
            "🛡️ *Oldini olish:*\n{prevention}"
        ),
        "severity": {
            "low": "🟢 Past xavf",
            "medium": "🟡 O'rtacha xavf",
            "high": "🔴 Yuqori xavf",
            "critical": "⛔ Kritik"
        },
        "btn_plant": "🌿 O'simlikni aniqlash",
        "btn_disease": "🦠 Kasallikni aniqlash",
        "btn_both": "🔍 Ikkala tahlil",
        "btn_web": "🌐 Web saytga o'tish",
        "btn_language": "🌍 Tilni o'zgartirish",
        "language_selected": "✅ Til o'zgartirildi: O'zbek 🇺🇿",
        "choose_language": "🌍 Tilni tanlang:",
        "error": "❌ Xatolik yuz berdi. Qayta urinib ko'ring.",
        "send_photo": "📸 Iltimos, rasm yuboring!",
        "about": (
            "ℹ️ *AgroVision AI Bot*\n\n"
            "🤖 Sun'iy intellekt asosida ishlaydi\n"
            "🧠 YOLOv8 + EfficientNet modellari\n"
            "🇺🇿 O'zbekiston qishloq xo'jaligi uchun\n\n"
            "🌐 Web: {web_url}"
        ),
        "no_photo": "❌ Rasm aniqlanmadi. Iltimos, to'g'ri rasm yuboring.",
        "cancel": "❌ Bekor qilindi",
    },
    "ru": {
        "welcome": (
            "🌿 *Добро пожаловать в AgroVision AI Bot!*\n\n"
            "Этот бот поможет вам с помощью ИИ:\n\n"
            "🔬 *Определить растение* — отправьте фото\n"
            "🦠 *Обнаружить болезнь* — фото листа/плода\n"
            "🌾 *Рекомендации по лечению* — при обнаружении болезни\n\n"
            "📸 *Отправьте фото, чтобы начать!*"
        ),
        "help": (
            "📖 *Справка*\n\n"
            "1️⃣ Отправьте фото (растение или лист)\n"
            "2️⃣ Выберите тип анализа\n"
            "3️⃣ Получите результат ИИ\n\n"
            "🌐 *Команды:*\n"
            "/start — Начало\n"
            "/help — Справка\n"
            "/language — Изменить язык\n"
            "/about — О боте"
        ),
        "choose_analysis": "📸 Фото получено! Выберите тип анализа:",
        "analyzing": "⏳ *Анализируется...*\nМодель ИИ работает, подождите немного.",
        "plant_result": (
            "🌿 *Растение определено!*\n\n"
            "📛 *Название:* {plant_name}\n"
            "🔬 *Научное название:* _{scientific_name}_\n"
            "🏷️ *Семейство:* {family}\n"
            "📊 *Достоверность:* *{confidence}%*\n\n"
            "📝 *Информация:*\n{description}\n\n"
            "🌱 *Сезон роста:* {growing_season}\n"
            "💧 *Потребность в воде:* {water_needs}\n\n"
            "📍 *Подходящие регионы в Узбекистане:*\n{regions}"
        ),
        "disease_result": (
            "🦠 *Болезнь обнаружена!*\n\n"
            "⚕️ *Болезнь:* {disease_name}\n"
            "🌿 *Поражённое растение:* {plant_affected}\n"
            "🚨 *Степень тяжести:* {severity}\n"
            "📊 *Достоверность:* *{confidence}%*\n\n"
            "📝 *Описание:*\n{description}\n\n"
            "⚠️ *Причины:*\n{causes}\n\n"
            "💊 *Рекомендации по лечению:*\n{treatments}\n\n"
            "🛡️ *Профилактика:*\n{prevention}"
        ),
        "severity": {
            "low": "🟢 Низкий риск",
            "medium": "🟡 Средний риск",
            "high": "🔴 Высокий риск",
            "critical": "⛔ Критический"
        },
        "btn_plant": "🌿 Определить растение",
        "btn_disease": "🦠 Обнаружить болезнь",
        "btn_both": "🔍 Оба анализа",
        "btn_web": "🌐 Перейти на сайт",
        "btn_language": "🌍 Изменить язык",
        "language_selected": "✅ Язык изменён: Русский 🇷🇺",
        "choose_language": "🌍 Выберите язык:",
        "error": "❌ Произошла ошибка. Попробуйте снова.",
        "send_photo": "📸 Пожалуйста, отправьте фото!",
        "about": (
            "ℹ️ *AgroVision AI Bot*\n\n"
            "🤖 Работает на искусственном интеллекте\n"
            "🧠 Модели YOLOv8 + EfficientNet\n"
            "🇺🇿 Для сельского хозяйства Узбекистана\n\n"
            "🌐 Сайт: {web_url}"
        ),
        "no_photo": "❌ Фото не обнаружено. Пожалуйста, отправьте корректное изображение.",
        "cancel": "❌ Отменено",
    },
    "en": {
        "welcome": (
            "🌿 *Welcome to AgroVision AI Bot!*\n\n"
            "This bot helps you with AI-powered agriculture:\n\n"
            "🔬 *Plant Detection* — send a photo\n"
            "🦠 *Disease Detection* — leaf/fruit photo\n"
            "🌾 *Treatment Advice* — when disease is detected\n\n"
            "📸 *Send a photo to get started!*"
        ),
        "help": (
            "📖 *Help*\n\n"
            "1️⃣ Send a photo (plant or leaf)\n"
            "2️⃣ Choose analysis type\n"
            "3️⃣ Get AI results\n\n"
            "🌐 *Commands:*\n"
            "/start — Start\n"
            "/help — Help\n"
            "/language — Change language\n"
            "/about — About bot"
        ),
        "choose_analysis": "📸 Photo received! Choose analysis type:",
        "analyzing": "⏳ *Analyzing...*\nAI model is processing, please wait.",
        "plant_result": (
            "🌿 *Plant Identified!*\n\n"
            "📛 *Name:* {plant_name}\n"
            "🔬 *Scientific name:* _{scientific_name}_\n"
            "🏷️ *Family:* {family}\n"
            "📊 *Confidence:* *{confidence}%*\n\n"
            "📝 *Description:*\n{description}\n\n"
            "🌱 *Growing Season:* {growing_season}\n"
            "💧 *Water Needs:* {water_needs}\n\n"
            "📍 *Suitable Regions in Uzbekistan:*\n{regions}"
        ),
        "disease_result": (
            "🦠 *Disease Detected!*\n\n"
            "⚕️ *Disease:* {disease_name}\n"
            "🌿 *Affected Plant:* {plant_affected}\n"
            "🚨 *Severity:* {severity}\n"
            "📊 *Confidence:* *{confidence}%*\n\n"
            "📝 *Description:*\n{description}\n\n"
            "⚠️ *Causes:*\n{causes}\n\n"
            "💊 *Treatment Recommendations:*\n{treatments}\n\n"
            "🛡️ *Prevention Tips:*\n{prevention}"
        ),
        "severity": {
            "low": "🟢 Low Risk",
            "medium": "🟡 Medium Risk",
            "high": "🔴 High Risk",
            "critical": "⛔ Critical"
        },
        "btn_plant": "🌿 Detect Plant",
        "btn_disease": "🦠 Detect Disease",
        "btn_both": "🔍 Both Analyses",
        "btn_web": "🌐 Open Website",
        "btn_language": "🌍 Change Language",
        "language_selected": "✅ Language changed: English 🇬🇧",
        "choose_language": "🌍 Choose language:",
        "error": "❌ An error occurred. Please try again.",
        "send_photo": "📸 Please send a photo!",
        "about": (
            "ℹ️ *AgroVision AI Bot*\n\n"
            "🤖 Powered by Artificial Intelligence\n"
            "🧠 YOLOv8 + EfficientNet models\n"
            "🇺🇿 For Uzbekistan Agriculture\n\n"
            "🌐 Website: {web_url}"
        ),
        "no_photo": "❌ No photo detected. Please send a valid image.",
        "cancel": "❌ Cancelled",
    },
}


def get_msg(lang: str, key: str, **kwargs) -> str:
    """Tilga qarab xabar matnini qaytaradi."""
    lang = lang if lang in MESSAGES else "uz"
    template = MESSAGES[lang].get(key, MESSAGES["en"].get(key, ""))
    if kwargs and isinstance(template, str):
        try:
            return template.format(**kwargs)
        except KeyError:
            return template
    return template
