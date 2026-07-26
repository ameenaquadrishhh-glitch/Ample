"""
YOLOv8 Violence Detection Service
"""
from models.schemas import DetectionResult
import cv2
import os

MODEL_PATH = os.getenv(
    "YOLO_MODEL_PATH",
    r"C:\Users\Ma qudri\OneDrive\Documents\AMPLE\runs\classify\runs\ample_v2\weights\best.pt"
)

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
    try:
        from ultralytics import YOLO
        model = YOLO(MODEL_PATH)

        cap = cv2.VideoCapture(video_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 25
        sample_every = max(1, int(fps))  # sample 1 frame per second

        max_conf = 0.0
        violence_frames = 0
        processed = 0
        frame_idx = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_idx % sample_every == 0:
                results = model(frame, verbose=False)
                for result in results:
                    probs = result.probs
                    if probs is not None:
                        # class 1 = violence (check your class order)
                        violence_conf = float(probs.data[1]) if len(probs.data) > 1 else float(probs.top1conf)
                        if violence_conf > max_conf:
                            max_conf = violence_conf
                        if violence_conf > 0.3:
                            violence_frames += 1
                processed += 1
            frame_idx += 1

        cap.release()

        violence_detected = max_conf > 0.3
        threat_level = get_threat_level(max_conf)
        summary = (
            f"Analyzed {processed} sampled frames out of {frame_count} total. "
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
        import traceback

    print("\n" + "=" * 80)
    print("DETECTION ERROR")
    print("=" * 80)
    traceback.print_exc()
    print("=" * 80 + "\n")

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