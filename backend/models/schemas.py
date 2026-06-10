from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class IncidentCreate(BaseModel):
    video_filename: str
    threat_level: str
    confidence_score: float
    violence_detected: bool
    frame_count: int
    detection_summary: str
    ai_report: Optional[str] = None
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None

class IncidentResponse(IncidentCreate):
    id: str
    created_at: datetime

class DetectionResult(BaseModel):
    violence_detected: bool
    confidence_score: float
    threat_level: str
    frame_count: int
    detection_summary: str
