from ultralytics import YOLO
import cv2
import os

model = YOLO("./models/best.pt")

VIOLENT_FOLDER = "./A-Dataset-for-Automatic-Violence-Detection-in-Videos/violence-detection-dataset/violent/cam1"
NONVIOLENT_FOLDER = "./A-Dataset-for-Automatic-Violence-Detection-in-Videos/violence-detection-dataset/non-violent/cam1"

def test_folder(folder_path, expected_label):
    videos = [f for f in os.listdir(folder_path) if f.endswith('.mp4')][:5]
    print(f"\nTesting {expected_label} clips ({len(videos)} videos)...")
    print("-" * 40)

    for video_name in videos:
        path = os.path.join(folder_path, video_name)
        cap = cv2.VideoCapture(path)
        alert_count = 0
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            if frame_count % 5 != 0:
                continue

            results = model(frame, device=0, verbose=False)
            for result in results:
                if result.boxes is not None:
                    for box in result.boxes:
                        conf = float(box.conf[0])
                        label = model.names[int(box.cls[0])]
                        if conf > 0.5:
                            alert_count += 1

            cv2.imshow("AMPLE Dataset Test", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        print(f"  {video_name} — {alert_count} detections in {frame_count} frames")

    cv2.destroyAllWindows()

test_folder(VIOLENT_FOLDER, "VIOLENT")
test_folder(NONVIOLENT_FOLDER, "NON-VIOLENT")

print("\nTest complete.")