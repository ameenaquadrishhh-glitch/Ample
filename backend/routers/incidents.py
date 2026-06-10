from fastapi import APIRouter, HTTPException
from core.database import get_supabase

router = APIRouter()

@router.get("/")
def list_incidents(limit: int = 20, offset: int = 0):
    """Get all incidents, newest first."""
    db = get_supabase()
    result = db.table("incidents") \
        .select("*") \
        .order("created_at", desc=True) \
        .range(offset, offset + limit - 1) \
        .execute()
    return {"incidents": result.data, "total": len(result.data)}

@router.get("/{incident_id}")
def get_incident(incident_id: str):
    """Get a single incident by ID."""
    db = get_supabase()
    result = db.table("incidents").select("*").eq("id", incident_id).execute()
    if not result.data:
        raise HTTPException(404, "Incident not found")
    return result.data[0]

@router.get("/stats/summary")
def get_stats():
    """Dashboard summary stats."""
    db = get_supabase()
    all_incidents = db.table("incidents").select("threat_level, violence_detected").execute()
    data = all_incidents.data
    return {
        "total": len(data),
        "violence_detected": sum(1 for d in data if d["violence_detected"]),
        "critical": sum(1 for d in data if d["threat_level"] == "CRITICAL"),
        "high": sum(1 for d in data if d["threat_level"] == "HIGH"),
        "medium": sum(1 for d in data if d["threat_level"] == "MEDIUM"),
        "low": sum(1 for d in data if d["threat_level"] == "LOW"),
    }
