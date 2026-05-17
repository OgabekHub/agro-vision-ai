#!/bin/bash

# Print environment info
echo "🌱 Starting AgroVision AI Unified Services..."
echo "Python version: $(python --version)"

# 1. Telegram Botni orqa fonda (background) ishga tushirish
echo "🤖 Starting Telegram Bot in background..."
python /code/telegram_bot/bot.py &

# 2. FastAPI Backendni asosiy jarayon (foreground) sifatida ishga tushirish
echo "🚀 Starting FastAPI Backend on port 7860..."
cd /code/backend
uvicorn app.main:app --host 0.0.0.0 --port 7860
