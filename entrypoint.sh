#!/bin/bash

# Print environment info
echo "🌱 Starting AgroVision AI Unified Services..."
echo "Python version: $(python --version)"

# 1. Telegram Botni orqa fonda (background) auto-restart bilan ishga tushirish
echo "🤖 Starting Telegram Bot with auto-restart..."
while true; do
    echo "🌿 Starting bot.py..." >> /code/bot.log
    python /code/telegram_bot/bot.py >> /code/bot.log 2>&1
    echo "⚠️ Bot exited. Restarting in 5 seconds..." >> /code/bot.log
    sleep 5
done &


# 2. FastAPI Backendni asosiy jarayon (foreground) sifatida ishga tushirish
echo "🚀 Starting FastAPI Backend on port 7860..."
cd /code/backend
uvicorn app.main:app --host 0.0.0.0 --port 7860
