import os
import sys
from dotenv import load_dotenv

# Load env from backend/.env
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend"))
load_dotenv(os.path.join(backend_dir, ".env"))

# Add backend to path
sys.path.append(backend_dir)

from app.core.supabase_service import get_supabase

def test_queries():
    client = get_supabase()
    if not client:
        print("[FAIL] Supabase client could not be initialized.")
        return

    print("[OK] Supabase client initialized.")

    tables = ["plant_analyses", "disease_analyses", "land_analyses", "users", "ai_logs"]

    for table in tables:
        print(f"\n--- Testing table: {table} ---")
        try:
            # Test count
            count_resp = client.table(table).select("id", count="exact").limit(1).execute()
            print(f"  Count check: SUCCESS, count = {count_resp.count}")
        except Exception as e:
            print(f"  Count check: FAILED - {e}")

        try:
            # Test select *
            select_resp = client.table(table).select("*").limit(1).execute()
            print(f"  Select * check: SUCCESS, rows returned = {len(select_resp.data)}")
            if select_resp.data:
                print(f"  Columns: {list(select_resp.data[0].keys())}")
        except Exception as e:
            print(f"  Select * check: FAILED - {e}")

if __name__ == "__main__":
    test_queries()
