import asyncio
import os
import httpx

API_KEY = "AIzaSyCaf9Sv74BJgjgusKVAiuiqFftjrECBvBw"
MODELS = ["gemini-2.5-flash", "gemini-2.0-flash-lite", "gemini-2.0-flash"]

async def test():
    for model in MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
        payload = {"contents": [{"parts": [{"text": "Say only: OK"}]}]}
        try:
            async with httpx.AsyncClient(timeout=20) as c:
                r = await c.post(url, json=payload)
                if r.status_code == 200:
                    text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                    print(f"OK {model}: {text.strip()}")
                    return
                else:
                    err = r.json().get("error", {})
                    code = err.get("code", r.status_code)
                    msg = err.get("message", "")[:100]
                    print(f"FAIL {model}: {code} - {msg}")
        except Exception as e:
            print(f"ERROR {model}: {e}")

asyncio.run(test())
