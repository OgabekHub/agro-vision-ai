import httpx
import asyncio

async def test():
    with open("test_leaf.jpg", "rb") as f:
        image_bytes = f.read()

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "http://localhost:8000/api/v1/disease/analyze",
            data={"language": "uz"},
            files={"file": ("test_leaf.jpg", image_bytes, "image/jpeg")},
            timeout=30.0
        )
        data = resp.json()
        print("FULL RESPONSE:")
        print(data)

if __name__ == "__main__":
    asyncio.run(test())
