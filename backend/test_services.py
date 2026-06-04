"""
Supabase, Cloudinary va OpenWeather API larni tekshiruvchi test skripti.
"""
import httpx
import json
import base64
import os

# .env faylidan o'qish
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# .env dan ma'lumotlar
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME", "")
CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY", "")
CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET", "")
OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")


def ok(msg): print(f"  [PASS] {msg}")
def fail(msg): print(f"  [FAIL] {msg}")
def info(msg): print(f"  [INFO] {msg}")
def header(msg): print(f"\n{'='*50}\n{msg}\n{'='*50}")


# ── 1. SUPABASE ────────────────────────────────────────
header("1. SUPABASE — Ma'lumotlar bazasi")
try:
    resp = httpx.get(
        f"{SUPABASE_URL}/rest/v1/",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
        },
        timeout=10
    )
    if resp.status_code in (200, 404, 400, 401):
        ok(f"Supabase ulanish mavjud — HTTP {resp.status_code}")
        info(f"URL: {SUPABASE_URL}")
    else:
        fail(f"Supabase ulanmadi — HTTP {resp.status_code}: {resp.text[:100]}")
except Exception as e:
    fail(f"Supabase xato: {e}")

# RLS xatosini tekshirish uchun jadvalga so'rov
try:
    resp = httpx.get(
        f"{SUPABASE_URL}/rest/v1/plant_analyses?limit=1",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
        },
        timeout=10
    )
    if resp.status_code == 200:
        data = resp.json()
        ok(f"plant_analyses jadvali o'qildi — {len(data)} qator")
    elif resp.status_code == 401:
        fail(f"Supabase — Autentifikatsiya xatosi (401). Kalit noto'g'ri.")
    else:
        info(f"plant_analyses — HTTP {resp.status_code} (RLS qo'llanilgan bo'lishi mumkin)")
except Exception as e:
    fail(f"Jadval so'rovida xato: {e}")


# ── 2. CLOUDINARY ─────────────────────────────────────
header("2. CLOUDINARY — Rasm CDN")
try:
    import hmac, hashlib, time
    timestamp = int(time.time())
    # Cloudinary ping endpoint
    resp = httpx.get(
        f"https://api.cloudinary.com/v1_1/{CLOUDINARY_CLOUD_NAME}/resources/image?max_results=1",
        auth=(CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET),
        timeout=10
    )
    if resp.status_code == 200:
        resources = resp.json().get("resources", [])
        ok(f"Cloudinary ishlayapdi! Saqlangan rasmlar: {len(resources)}+ ta")
        if resources:
            info(f"Oxirgi rasm: {resources[0].get('public_id', '?')}")
    elif resp.status_code == 401:
        fail(f"Cloudinary — API key noto'g'ri (401)")
    else:
        fail(f"Cloudinary — HTTP {resp.status_code}: {resp.text[:100]}")
except Exception as e:
    fail(f"Cloudinary xato: {e}")

# Upload test
try:
    with open("test_leaf.jpg", "rb") as f:
        img_data = f.read()
    
    import hmac, hashlib, time
    timestamp = int(time.time())
    sig_str = f"folder=agrovision&timestamp={timestamp}{CLOUDINARY_API_SECRET}"
    signature = hashlib.sha1(sig_str.encode()).hexdigest()
    
    resp = httpx.post(
        f"https://api.cloudinary.com/v1_1/{CLOUDINARY_CLOUD_NAME}/image/upload",
        data={
            "api_key": CLOUDINARY_API_KEY,
            "timestamp": timestamp,
            "signature": signature,
            "folder": "agrovision",
        },
        files={"file": ("test.jpg", img_data, "image/jpeg")},
        timeout=20
    )
    if resp.status_code == 200:
        url = resp.json().get("secure_url", "?")
        ok(f"Cloudinary upload muvaffaqiyatli!")
        info(f"URL: {url[:70]}...")
    else:
        fail(f"Cloudinary upload xato — HTTP {resp.status_code}: {resp.text[:100]}")
except Exception as e:
    fail(f"Cloudinary upload xato: {e}")


# ── 3. OPENWEATHER ────────────────────────────────────
header("3. OPENWEATHER — Ob-havo API")
try:
    resp = httpx.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={
            "q": "Tashkent,UZ",
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
            "lang": "en" # Use English to avoid Windows console Cyrillic encoding crashes
        },
        timeout=10
    )
    if resp.status_code == 200:
        data = resp.json()
        temp = data.get("main", {}).get("temp", "?")
        desc = data.get("weather", [{}])[0].get("description", "?")
        city = data.get("name", "?")
        ok(f"OpenWeather ishlayapdi!")
        info(f"Shahar: {city}")
        info(f"Harorat: {temp}C")
        info(f"Holat: {desc}")
    elif resp.status_code == 401:
        fail(f"OpenWeather — API key noto'g'ri yoki faol emas (401)")
    else:
        fail(f"OpenWeather — HTTP {resp.status_code}: {resp.text[:100]}")
except Exception as e:
    fail(f"OpenWeather xato: {e}")


# ── YAKUNIY ───────────────────────────────────────────
print(f"\n{'='*50}")
print("TEKSHIRUV YAKUNLANDI")
print(f"{'='*50}\n")
