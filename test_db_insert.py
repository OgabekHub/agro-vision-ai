import os
import sys
from dotenv import load_dotenv

# Load env from backend/.env
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend"))
load_dotenv(os.path.join(backend_dir, ".env"))

# Add backend to path
sys.path.append(backend_dir)

from app.core.supabase_service import get_supabase

def test_inserts():
    client = get_supabase()
    if not client:
        print("[FAIL] Supabase client could not be initialized.")
        return

    print("[OK] Supabase client initialized.")

    # 1. Test insert to disease_analyses
    row = {
        "image_url": "https://example.com/test.jpg",
        "disease_name": "Test Disease",
        "plant_affected": "Test Plant",
        "confidence": 0.95,
        "severity": "low",
        "description": "Test description",
        "causes": ["cause1"],
        "symptoms": ["symptom1"],
        "treatments": ["treatment1"],
        "prevention_tips": ["tip1"],
        "model_version": "test_model",
        "processing_time_ms": 100,
    }

    print("\nTrying to insert into disease_analyses...")
    try:
        resp = client.table("disease_analyses").insert(row).execute()
        print("🎉 Insert into disease_analyses SUCCESS!")
        print(f"Returned data: {resp.data}")
        # Clean up
        if resp.data:
            inserted_id = resp.data[0]["id"]
            client.table("disease_analyses").delete().eq("id", inserted_id).execute()
            print("Cleanup delete successful.")
    except Exception as e:
        print(f"❌ Insert into disease_analyses FAILED: {e}")

    # 2. Test insert to ai_logs
    log_row = {
        "analysis_type": "disease",
        "result": {"disease_name": "Test Disease"},
        "confidence": 0.95,
        "processing_time_ms": 100,
        "model_version": "test_model",
    }

    print("\nTrying to insert into ai_logs...")
    try:
        resp = client.table("ai_logs").insert(log_row).execute()
        print("🎉 Insert into ai_logs SUCCESS!")
        print(f"Returned data: {resp.data}")
        if resp.data:
            inserted_id = resp.data[0]["id"]
            client.table("ai_logs").delete().eq("id", inserted_id).execute()
            print("Cleanup delete successful.")
    except Exception as e:
        print(f"❌ Insert into ai_logs FAILED: {e}")

if __name__ == "__main__":
    test_inserts()
