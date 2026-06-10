from fastapi import APIRouter, UploadFile, File, HTTPException
from services.detection import run_detection
from services.report_gen import generate_report
from services.alert import send_alerts
from core.database import get_supabase
from models.schemas import IncidentCreate
import tempfile, os

router = APIRouter()

@router.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    """
    Upload a video file, run YOLOv8 detection,
    generate an AI incident report, and save to DB.
    """
    if not file.filename.endswith(('.mp4', '.avi', '.mov')):
        raise HTTPException(400, "Invalid file type. Use mp4, avi, or mov.")

    # Save upload to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        # Step 1: Run YOLOv8 detection
        detection = run_detection(tmp_path)

        # Step 2: Generate AI report
        report = generate_report(detection, file.filename)

        # Step 3: Save to Supabase
        incident_data = IncidentCreate(
            video_filename=file.filename,
            threat_level=detection.threat_level,
            confidence_score=detection.confidence_score,
            violence_detected=detection.violence_detected,
            frame_count=detection.frame_count,
            detection_summary=detection.detection_summary,
            ai_report=report,
        )
        db = get_supabase()
        result = db.table("incidents").insert(incident_data.model_dump()).execute()
        incident_id = result.data[0]["id"]

        # Step 4: Send alerts if HIGH or CRITICAL
        if detection.threat_level in ["HIGH", "CRITICAL"]:
            send_alerts(incident_data, incident_id)

        return {"status": "success", "incident_id": incident_id, "detection": detection, "report": report}

    finally:
        os.unlink(tmp_path)
