"""
Barcha API endpointlarni to'liq tekshiruvchi test skripti.
Tests: /plant/detect, /disease/analyze, /recommend/crops
"""
import httpx
import asyncio
import json
import sys
import os

BASE_URL = "http://localhost:8000"
TEST_LEAF = "test_leaf.jpg"

COLORS = {
    "green": "\033[92m",
    "red": "\033[91m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "cyan": "\033[96m",
    "reset": "\033[0m",
    "bold": "\033[1m",
}

def ok(msg): print(f"{COLORS['green']}  [PASS]{COLORS['reset']} {msg}")
def fail(msg): print(f"{COLORS['red']}  [FAIL]{COLORS['reset']} {msg}")
def info(msg): print(f"{COLORS['cyan']}  [INFO]{COLORS['reset']} {msg}")
def header(msg): print(f"\n{COLORS['bold']}{COLORS['blue']}{'='*55}\n{msg}\n{'='*55}{COLORS['reset']}")


async def test_plant(client: httpx.AsyncClient, image_bytes: bytes) -> bool:
    header("1. O'SIMLIK ANIQLASH — /api/v1/plant/detect")
    try:
        resp = await client.post(
            f"{BASE_URL}/api/v1/plant/detect",
            files={"file": ("test_leaf.jpg", image_bytes, "image/jpeg")},
            data={"language": "uz"},
            timeout=60.0
        )
        if resp.status_code != 200:
            fail(f"HTTP {resp.status_code}")
            print(resp.text)
            return False

        data = resp.json().get("data", {})
        plant_name = data.get("plant_name", "Yo'q")
        confidence = data.get("confidence", 0)
        model = data.get("model_version", "unknown")
        is_plant = data.get("is_plant", False)
        top3 = data.get("top3_predictions", [])

        ok(f"HTTP 200 OK — Model: {model}")
        info(f"O'simlik nomi : {plant_name}")
        info(f"Aniqlik       : {confidence*100:.1f}%")
        info(f"O'simlikmi?   : {is_plant}")
        if top3:
            info(f"Top-3         : {[t['class'] for t in top3[:3]]}")

        if not plant_name or plant_name in ["Yo'q", "Noma'lum"]:
            fail("O'simlik aniqlanmadi!")
            return False
        if confidence < 0.3:
            fail(f"Aniqlik juda past: {confidence:.2%}")
            return False

        ok("O'simlik aniqlash muvaffaqiyatli!")
        return True
    except Exception as e:
        fail(f"Xato: {e}")
        return False


async def test_disease(client: httpx.AsyncClient, image_bytes: bytes) -> bool:
    header("2. KASALLIK ANIQLASH — /api/v1/disease/analyze")
    try:
        resp = await client.post(
            f"{BASE_URL}/api/v1/disease/analyze",
            files={"file": ("test_leaf.jpg", image_bytes, "image/jpeg")},
            data={"language": "uz"},
            timeout=60.0
        )
        if resp.status_code != 200:
            fail(f"HTTP {resp.status_code}")
            print(resp.text)
            return False

        data = resp.json().get("data", {})
        disease_name = data.get("disease_name", "Yo'q")
        plant = data.get("plant_affected", "Noma'lum")
        confidence = data.get("confidence", 0)
        severity = data.get("severity", "—")
        model = data.get("model_version", "unknown")
        top3 = data.get("top3_predictions", [])
        has_disease = data.get("has_disease", False)

        ok(f"HTTP 200 OK — Model: {model}")
        info(f"O'simlik      : {plant}")
        info(f"Kasallik      : {disease_name}")
        info(f"Aniqlik       : {confidence*100:.1f}%")
        info(f"Og'irlik      : {severity}")
        info(f"Kasalmi?      : {has_disease}")
        if top3:
            info(f"Top-3         : {[t['class'] for t in top3[:3]]}")

        if disease_name in ["AI sozlanmagan", "Yo'q", ""]:
            fail("Kasallik aniqlanmadi (mock javob qaytdi)!")
            return False
        if confidence < 0.3:
            fail(f"Aniqlik juda past: {confidence:.2%}")
            return False

        ok("Kasallik aniqlash muvaffaqiyatli!")
        return True
    except Exception as e:
        fail(f"Xato: {e}")
        return False


async def test_land(client: httpx.AsyncClient, image_bytes: bytes) -> bool:
    header("3. YER TAHLILI — /api/v1/recommend/crops")
    try:
        resp = await client.post(
            f"{BASE_URL}/api/v1/recommend/crops",
            files={"file": ("test_leaf.jpg", image_bytes, "image/jpeg")},
            data={"language": "uz", "region": "Tashkent"},
            timeout=60.0
        )
        if resp.status_code != 200:
            fail(f"HTTP {resp.status_code}")
            print(resp.text)
            return False

        data = resp.json().get("data", {})
        soil = data.get("soil_condition", {})
        crops = data.get("recommended_crops", [])
        suggestions = data.get("farming_suggestions", [])
        model = data.get("model_version", "unknown")

        ok(f"HTTP 200 OK — Model: {model}")
        info(f"Tuproq turi   : {soil.get('type', '—')}")
        info(f"pH darajasi   : {soil.get('ph_level', '—')}")
        info(f"Namlik        : {soil.get('moisture', '—')}")
        info(f"Tavsiya ekinlar: {[c.get('crop_name') for c in crops[:3]]}")
        info(f"Tavsiyalar soni: {len(suggestions)}")

        if not crops:
            fail("Ekinlar tavsiyasi bo'sh!")
            return False

        ok("Yer tahlili muvaffaqiyatli!")
        return True
    except Exception as e:
        fail(f"Xato: {e}")
        return False


async def main():
    print(f"\n{COLORS['bold']}{COLORS['cyan']}AgroVision AI — To'liq API Test{COLORS['reset']}")
    print(f"Backend: {BASE_URL}")

    if not os.path.exists(TEST_LEAF):
        fail(f"Test rasmi topilmadi: {TEST_LEAF}")
        sys.exit(1)

    with open(TEST_LEAF, "rb") as f:
        image_bytes = f.read()
    info(f"Test rasmi: {TEST_LEAF} ({len(image_bytes)/1024:.1f} KB)")

    results = {}
    async with httpx.AsyncClient() as client:
        results["plant"] = await test_plant(client, image_bytes)
        results["disease"] = await test_disease(client, image_bytes)
        results["land"] = await test_land(client, image_bytes)

    # Summary
    header("YAKUNIY NATIJALAR")
    passed = sum(results.values())
    total = len(results)
    for name, result in results.items():
        label = {
            "plant": "O'simlik aniqlash",
            "disease": "Kasallik aniqlash",
            "land": "Yer tahlili"
        }[name]
        if result:
            ok(f"{label}")
        else:
            fail(f"{label}")

    print()
    if passed == total:
        print(f"{COLORS['green']}{COLORS['bold']}  BARCHA {total}/{total} TEST MUVAFFAQIYATLI!{COLORS['reset']}")
    else:
        print(f"{COLORS['yellow']}{COLORS['bold']}  {passed}/{total} TEST MUVAFFAQIYATLI — {total - passed} ta muvaffaqiyatsiz.{COLORS['reset']}")

if __name__ == "__main__":
    asyncio.run(main())
