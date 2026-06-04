import os
import sys
from dotenv import load_dotenv

# Load env from backend/.env
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend"))
load_dotenv(os.path.join(backend_dir, ".env"))

# Add backend to path
sys.path.append(backend_dir)

from app.core.supabase_service import get_supabase

def test_logs_query():
    client = get_supabase()
    if not client:
        print("[FAIL] Supabase client could not be initialized.")
        return

    print("[OK] Supabase client initialized.")

    start = 0
    end = 19

    try:
        print("Running query: client.table('ai_logs').select('*', count='exact').order('created_at', desc=True).range(start, end).execute()")
        response = client.table("ai_logs").select("*", count="exact").order("created_at", desc=True).range(start, end).execute()
        print(f"Query succeeded! count={response.count}, data_len={len(response.data)}")
    except Exception as e:
        print(f"Query failed! Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_logs_query()
