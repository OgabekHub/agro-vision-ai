"""
To'liq Gemini API key tekshiruvi — rasm bilan test
"""
import httpx
import base64
import json
import os

# API key .env dan o'qiladi
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
key = os.environ.get("GEMINI_API_KEY", "")
if not key:
    print("[XATO] GEMINI_API_KEY .env faylida topilmadi!")
    exit(1)
models = ['gemini-2.5-flash', 'gemini-2.0-flash-lite', 'gemini-2.0-flash', 'gemini-2.5-pro']

print(f"API Key: {key[:20]}...")
print()

# Load test image
with open("test_leaf.jpg", "rb") as f:
    img_bytes = f.read()
b64_img = base64.b64encode(img_bytes).decode()

print(f"Test rasmi: test_leaf.jpg ({len(img_bytes)//1024} KB)")
print()

working_model = None
for model in models:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    payload = {
        "contents": [{
            "parts": [
                {"text": "What plant is in this image? Reply in 1 short sentence."},
                {"inlineData": {"mimeType": "image/jpeg", "data": b64_img}}
            ]
        }],
        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 100}
    }
    try:
        resp = httpx.post(url, json=payload, timeout=30)
        if resp.status_code == 200:
            resp_data = resp.json()
            model_version = resp_data.get("modelVersion", model)
            candidates = resp_data.get("candidates", [])
            text = ""
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                for p in parts:
                    if "text" in p and not p.get("thought"):
                        text = p["text"].strip()
                        break
            if text:
                print(f"  [OK] {model} ishlamoqda!")
                print(f"       ModelVersion: {model_version}")
                print(f"       Javob: {text[:100]}")
            else:
                print(f"  [WARN] {model} javob berdi lekin matn bo'sh (parts: {len(parts)})")
                print(f"         FinishReason: {candidates[0].get('finishReason', '?') if candidates else 'no candidates'}")
            working_model = model
            break
        else:
            err = resp.json().get("error", {})
            status = err.get("status", "UNKNOWN")
            message = err.get("message", "")[:90]
            print(f"  [FAIL] {model} -> {resp.status_code} {status}: {message}")
    except Exception as e:
        print(f"  [ERR] {model} -> {type(e).__name__}: {e}")

print()
if working_model:
    print(f"[NATIJA] Ishlayotgan model: {working_model}")
    print("[NATIJA] Gemini API KEY ISHLAYAPDI!")
else:
    print("[NATIJA] Hech bir model ishlamadi! API key noto'g'ri yoki limit tugagan.")
