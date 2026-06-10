"""
YOLOv8 Violence Detection Service
Wraps your existing detection logic into a clean service layer.
"""
from models.schemas import DetectionResult
import cv2
import os

# Model path — update this to your actual .pt file location
MODEL_PATH = os.getenv("YOLO_MODEL_PATH", "yolov8n.pt")

def get_threat_level(confidence: float) -> str:
    if confidence >= 0.85:
        return "CRITICAL"
    elif confidence >= 0.60:
        return "HIGH"
    elif confidence >= 0.30:
        return "MEDIUM"
    else:
        return "LOW"

def run_detection(video_path: str) -> DetectionResult:
    """
    Run YOLOv8 on a video file and return structured detection results.
    Falls back to OpenCV frame count if model not available.
    """
    try:
        from ultralytics import YOLO
        model = YOLO(MODEL_PATH)
        results = model(video_path, stream=True, verbose=False)

        max_conf = 0.0
        frame_count = 0
        violence_frames = 0

        for result in results:
            frame_count += 1
            for box in result.boxes:
                conf = float(box.conf[0])
                if conf > max_conf:
                    max_conf = conf
                if conf > 0.3:
                    violence_frames += 1

        violence_detected = max_conf > 0.3
        threat_level = get_threat_level(max_conf)

        summary = (
            f"Analyzed {frame_count} frames. "
            f"{'Violence detected' if violence_detected else 'No violence detected'} "
            f"with peak confidence {max_conf:.2%}. "
            f"{violence_frames} frames flagged."
        )

        return DetectionResult(
            violence_detected=violence_detected,
            confidence_score=round(max_conf, 4),
            threat_level=threat_level,
            frame_count=frame_count,
            detection_summary=summary,
        )

    except Exception as e:
        # Fallback: count frames only
        cap = cv2.VideoCapture(video_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        return DetectionResult(
            violence_detected=False,
            confidence_score=0.0,
            threat_level="LOW",
            frame_count=frame_count,
            detection_summary=f"Detection error: {str(e)}. Frame count only.",
        )
