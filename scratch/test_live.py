import httpx
import asyncio
import os

BASE_URL = "https://ogabekolimjonov-agro-vision-ai.hf.space"
TEST_LEAF = "backend/test_leaf.jpg"

if not os.path.exists(TEST_LEAF):
    # Fallback to test_leaf in parent if running from scratch directory
    TEST_LEAF = "../backend/test_leaf.jpg"

async def test_endpoint(client, name, path, files=None, data=None):
    url = f"{BASE_URL}{path}"
    print(f"Testing {name} ({url})...")
    try:
        if files:
            resp = await client.post(url, files=files, data=data, timeout=30.0)
        elif data:
            resp = await client.post(url, json=data, timeout=30.0)
        else:
            resp = await client.get(url, timeout=30.0)
        
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            print(f"[PASS] {name} PASSED")
            try:
                print(f"Response snippet: {str(resp.json())[:300]}...")
            except Exception:
                print(f"Response snippet: {resp.text[:300]}...")
            return True
        else:
            print(f"[FAIL] {name} FAILED: HTTP {resp.status_code}")
            print(resp.text)
            return False
    except Exception as e:
        print(f"[FAIL] {name} FAILED with exception: {e}")
        return False

async def main():
    print(f"==================================================")
    print(f"Testing Live AgroVision AI Backend at:")
    print(f"{BASE_URL}")
    print(f"==================================================")
    
    if not os.path.exists(TEST_LEAF):
        print(f"Error: test_leaf.jpg not found at {TEST_LEAF}!")
        return

    with open(TEST_LEAF, "rb") as f:
        image_bytes = f.read()

    async with httpx.AsyncClient(follow_redirects=True) as client:
        # 1. Health check
        await test_endpoint(client, "1. HEALTH CHECK", "/health")
        
        print("\n" + "="*40 + "\n")
        
        # 2. Plant detection
        files = {"file": ("test_leaf.jpg", image_bytes, "image/jpeg")}
        await test_endpoint(client, "2. PLANT DETECTION", "/api/v1/plant/detect", files=files, data={"language": "uz"})
        
        print("\n" + "="*40 + "\n")
        
        # 3. Disease analysis
        files = {"file": ("test_leaf.jpg", image_bytes, "image/jpeg")}
        await test_endpoint(client, "3. DISEASE ANALYSIS", "/api/v1/disease/analyze", files=files, data={"language": "uz"})
        
        print("\n" + "="*40 + "\n")
        
        # 4. Crop recommendations (Land analysis)
        files = {"file": ("test_leaf.jpg", image_bytes, "image/jpeg")}
        await test_endpoint(client, "4. LAND ANALYSIS", "/api/v1/recommend/crops", files=files, data={"language": "uz", "region": "Tashkent"})
        
        print("\n" + "="*40 + "\n")
        
        # 5. Weather
        await test_endpoint(client, "5. WEATHER", "/api/v1/weather/Tashkent")
        
        print("\n" + "="*40 + "\n")
        
        # 6. Regions
        await test_endpoint(client, "6. REGIONS", "/api/v1/regions")

if __name__ == "__main__":
    asyncio.run(main())
