import httpx

def test_space_gemini():
    url = "https://ogabekolimjonov-agro-vision-ai.hf.space/api/v1/disease/analyze"
    img_path = "backend/test_leaf.jpg"
    
    try:
        with open(img_path, "rb") as f:
            files = {"file": ("test_leaf.jpg", f, "image/jpeg")}
            data = {"language": "uz"}
            
            print(f"Sending test_leaf.jpg to {url}...")
            resp = httpx.post(url, files=files, data=data, timeout=60.0)
            
            print(f"Status Code: {resp.status_code}")
            if resp.status_code == 200:
                resp_json = resp.json()
                print("Response JSON:")
                import pprint
                pprint.pprint(resp_json)
            else:
                print(f"Error Response: {resp.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_space_gemini()
