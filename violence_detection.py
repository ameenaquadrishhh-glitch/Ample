from ultralytics import YOLO
import cv2
import time

# Load YOUR custom trained AMPLE model
model = YOLO("./runs/classify/runs/ample_v2/weights/best.pt")
cap = cv2.VideoCapture(0)

print("=" * 50)
print("  AMPLE Detection Engine — Custom Model v1.0")
print("  Accuracy: 92.5%  |  Press Q to quit")
print("=" * 50)

frame_count = 0
current_label = "Analyzing..."
current_conf = 0.0
alert_cooldown = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    if frame_count % 5 == 0:
        results = model(frame, verbose=False)

        if results and results[0].probs is not None:
            probs = results[0].probs
            top1_idx = int(probs.top1)
            top1_conf = float(probs.top1conf)
            current_label = model.names[top1_idx]
            current_conf = top1_conf

            # Fire alert if violent
            if current_label == "violent" and top1_conf > 0.7:
                if alert_cooldown == 0:
                    print(f"[!! ALERT !!] VIOLENCE DETECTED | Confidence: {top1_conf:.0%} | {time.strftime('%H:%M:%S')}")
                    alert_cooldown = 30
            else:
                if alert_cooldown > 0:
                    alert_cooldown -= 1

    # Choose colors
    if current_label == "violent":
        color = (0, 0, 255)
        status_text = "!! THREAT DETECTED !!"
        bar_color = (0, 0, 180)
    else:
        color = (0, 200, 0)
        status_text = "SCENE NORMAL"
        bar_color = (0, 140, 0)

    # Top header bar
    cv2.rectangle(frame, (0, 0), (frame.shape[1], 50), (15, 15, 15), -1)
    cv2.putText(frame,
                "AMPLE  |  AI Monitoring Platform for Live Emergency Detection",
                (10, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 200, 255), 2)

    # Status box in center
    cv2.rectangle(frame, (0, 55), (frame.shape[1], 100), bar_color, -1)
    cv2.putText(frame,
                f"  {status_text}   |   {current_label.upper()}  {current_conf:.0%}",
                (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

    # Bottom bar
    cv2.rectangle(frame,
                  (0, frame.shape[0] - 35),
                  (frame.shape[1], frame.shape[0]),
                  (15, 15, 15), -1)
    cv2.putText(frame,
                f"Camera: CAM-01  |  Model: AMPLE-v1  |  {time.strftime('%Y-%m-%d  %H:%M:%S')}",
                (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (150, 150, 150), 1)

    cv2.imshow("AMPLE - Violence Detection System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("AMPLE stopped.")