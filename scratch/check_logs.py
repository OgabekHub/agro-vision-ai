import os
import sys
from dotenv import load_dotenv

backend_dir = os.path.abspath("backend")
load_dotenv(os.path.join(backend_dir, ".env"))
sys.path.append(backend_dir)

from app.core.supabase_service import get_supabase

def check_logs():
    client = get_supabase()
    if not client:
        print("Failed to initialize Supabase client")
        return
    
    logs = client.table("ai_logs").select("*").order("created_at", desc=True).limit(5).execute().data
    print(f"Total retrieved: {len(logs)}\n")
    for i, l in enumerate(logs):
        print(f"[{i}] Created at: {l.get('created_at')}")
        print(f"    Type: {l.get('analysis_type')}")
        print(f"    Model Version: {l.get('model_version')}")
        print(f"    Confidence: {l.get('confidence')}")
        res = l.get("result", {})
        print(f"    Disease Name: {res.get('disease_name') or res.get('plant_name')}")
        print(f"    Severity: {res.get('severity')}")
        print(f"    Description: {res.get('description', '')[:150]}")
        print(f"    Causes count: {len(res.get('causes', [])) if isinstance(res.get('causes'), list) else 'N/A'}")
        print(f"    Treatments count: {len(res.get('treatments', [])) if isinstance(res.get('treatments'), list) else 'N/A'}")
        print("-" * 50)

if __name__ == "__main__":
    check_logs()
