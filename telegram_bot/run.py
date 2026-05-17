#!/usr/bin/env python3
"""
AgroVision AI Telegram Bot — O'rnatish va ishga tushirish skripti
"""

import subprocess
import sys
import os


def install_deps():
    print("📦 Kutubxonalar o'rnatilmoqda...")
    bot_dir = os.path.dirname(__file__)
    req_file = os.path.join(bot_dir, "requirements.txt")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
    print("✅ O'rnatish tugadi!\n")


def run_bot():
    print("🌿 AgroVision AI Bot ishga tushmoqda...")
    bot_dir = os.path.dirname(__file__)
    bot_file = os.path.join(bot_dir, "bot.py")
    os.chdir(bot_dir)
    subprocess.run([sys.executable, bot_file])


if __name__ == "__main__":
    if "--install" in sys.argv:
        install_deps()
    run_bot()
