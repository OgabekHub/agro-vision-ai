"""Supabase integration service."""

import logging
from typing import Optional, List, Dict, Any
from supabase import create_client, Client
from app.core.config import settings

logger = logging.getLogger(__name__)

_client: Optional[Client] = None


def get_supabase() -> Optional[Client]:
    """Initialize and return a fresh Supabase client instance."""
    url = settings.SUPABASE_URL
    key = settings.SUPABASE_KEY

    if not url or not key or "your_supabase" in url or "your_supabase" in key:
        logger.warning("Supabase URL or Key is not configured. Database logging is disabled.")
        return None

    try:
        client = create_client(url, key)
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")
        return None


async def log_plant_analysis(
    user_id: Optional[str],
    image_url: str,
    plant_name: str,
    scientific_name: str,
    family: str,
    confidence: float,
    description: str,
    suitable_regions: List[str],
    growing_season: str,
    water_needs: str,
    model_version: str,
    processing_time_ms: int,
) -> Optional[str]:
    """Save plant detection entry to plant_analyses table."""
    client = get_supabase()
    if not client:
        return None

    row = {
        "image_url": image_url,
        "plant_name": plant_name,
        "scientific_name": scientific_name,
        "family": family,
        "confidence": confidence,
        "description": description,
        "suitable_regions": suitable_regions,
        "growing_season": growing_season,
        "water_needs": water_needs,
        "model_version": model_version,
        "processing_time_ms": processing_time_ms,
    }
    if user_id:
        row["user_id"] = user_id

    try:
        # Run synchronously in run_in_executor if needed, but supabase-py supports async
        # We can just call it synchronously or run via run_in_threadpool since supabase-py is synchronous blocking.
        # So we run standard client call:
        response = client.table("plant_analyses").insert(row).execute()
        if response.data:
            analysis_id = response.data[0]["id"]
            return analysis_id
    except Exception as e:
        logger.error(f"Error saving plant analysis to Supabase: {e}")
    return None


async def log_disease_analysis(
    user_id: Optional[str],
    image_url: str,
    disease_name: str,
    plant_affected: str,
    confidence: float,
    severity: str,
    description: str,
    causes: List[str],
    symptoms: List[str],
    treatments: List[str],
    prevention_tips: List[str],
    model_version: str,
    processing_time_ms: int,
) -> Optional[str]:
    """Save disease analysis entry to disease_analyses table."""
    client = get_supabase()
    if not client:
        return None

    # Validate severity mapping to fit database check constraint: 'low', 'medium', 'high', 'critical'
    severity_val = severity.lower()
    if severity_val not in ["low", "medium", "high", "critical"]:
        severity_val = "medium"

    row = {
        "image_url": image_url,
        "disease_name": disease_name,
        "plant_affected": plant_affected,
        "confidence": confidence,
        "severity": severity_val,
        "description": description,
        "causes": causes,
        "symptoms": symptoms,
        "treatments": treatments,
        "prevention_tips": prevention_tips,
        "model_version": model_version,
        "processing_time_ms": processing_time_ms,
    }
    if user_id:
        row["user_id"] = user_id

    try:
        response = client.table("disease_analyses").insert(row).execute()
        if response.data:
            return response.data[0]["id"]
    except Exception as e:
        logger.error(f"Error saving disease analysis to Supabase: {e}")
    return None


async def log_land_analysis(
    user_id: Optional[str],
    image_url: str,
    soil_condition: Dict[str, Any],
    region: str,
    recommended_crops: List[Dict[str, Any]],
    farming_suggestions: List[str],
    irrigation_advice: str,
    model_version: str,
    processing_time_ms: int,
) -> Optional[str]:
    """Save crop recommendation/land analysis entry to land_analyses table."""
    client = get_supabase()
    if not client:
        return None

    row = {
        "image_url": image_url,
        "soil_condition": soil_condition,
        "region": region,
        "recommended_crops": recommended_crops,
        "farming_suggestions": farming_suggestions,
        "irrigation_advice": irrigation_advice,
        "model_version": model_version,
        "processing_time_ms": processing_time_ms,
    }
    if user_id:
        row["user_id"] = user_id

    try:
        response = client.table("land_analyses").insert(row).execute()
        if response.data:
            return response.data[0]["id"]
    except Exception as e:
        logger.error(f"Error saving land analysis to Supabase: {e}")
    return None


async def insert_ai_log(
    analysis_type: str,
    analysis_id: Optional[str],
    input_image_url: Optional[str],
    result: Dict[str, Any],
    confidence: float,
    processing_time_ms: int,
    model_version: str,
    error_message: Optional[str] = None,
) -> Optional[str]:
    """Write entry to ai_logs table."""
    client = get_supabase()
    if not client:
        return None

    row = {
        "analysis_type": analysis_type,
        "result": result,
        "confidence": confidence,
        "processing_time_ms": processing_time_ms,
        "model_version": model_version,
    }
    if analysis_id:
        row["analysis_id"] = analysis_id
    if input_image_url:
        row["input_image_url"] = input_image_url
    if error_message:
        row["error_message"] = error_message

    try:
        response = client.table("ai_logs").insert(row).execute()
        if response.data:
            return response.data[0]["id"]
    except Exception as e:
        logger.error(f"Error inserting AI log: {e}")
    return None
