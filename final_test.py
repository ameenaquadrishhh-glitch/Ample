from ultralytics import YOLO
import cv2
import os
import time

model = YOLO("./runs/classify/runs/ample_v2/weights/best.pt")

VIOLENT_DIR = "./A-Dataset-for-Automatic-Violence-Detection-in-Videos/violence-detection-dataset/violent/cam1"
NONVIOLENT_DIR = "./A-Dataset-for-Automatic-Violence-Detection-in-Videos/violence-detection-dataset/non-violent/cam1"

def test_folder(folder_path, expected, test_count=10):
    videos = [f for f in os.listdir(folder_path) if f.endswith('.mp4')][:test_count]
    
    correct = 0
    wrong = 0
    total_clips = 0

    print(f"\nTesting {expected.upper()} clips...")
    print("-" * 50)

    for video_name in videos:
        path = os.path.join(folder_path, video_name)
        cap = cv2.VideoCapture(path)
        
        violent_votes = 0
        nonviolent_votes = 0
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            if frame_count % 5 != 0:
                continue

            results = model(frame, verbose=False)

            if results and results[0].probs is not None:
                probs = results[0].probs
                label = model.names[int(probs.top1)]
                conf = float(probs.top1conf)

                if label == "violent":
                    violent_votes += 1
                else:
                    nonviolent_votes += 1

            # Show live detection
            color = (0, 0, 255) if violent_votes > nonviolent_votes else (0, 200, 0)
            status = "VIOLENT" if violent_votes > nonviolent_votes else "NONVIOLENT"
            cv2.rectangle(frame, (0, 0), (frame.shape[1], 50), (15, 15, 15), -1)
            cv2.putText(frame,
                        f"AMPLE  |  Testing: {video_name}  |  {status}",
                        (10, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 200, 255), 2)
            cv2.rectangle(frame, (0, 55), (frame.shape[1], 95), color, -1)
            cv2.putText(frame,
                        f"  Violent votes: {violent_votes}  |  Nonviolent votes: {nonviolent_votes}",
                        (10, 82), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.imshow("AMPLE - Model Testing", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()

        # Final verdict for this clip
        final = "violent" if violent_votes > nonviolent_votes else "nonviolent"
        is_correct = final == expected

        if is_correct:
            correct += 1
            result = "CORRECT"
        else:
            wrong += 1
            result = "WRONG"

        total_clips += 1
        print(f"  [{result}] {video_name} → predicted: {final.upper()} (V:{violent_votes} NV:{nonviolent_votes})")

    cv2.destroyAllWindows()

    accuracy = (correct / total_clips) * 100 if total_clips > 0 else 0
    print(f"\n  Result: {correct}/{total_clips} correct — {accuracy:.1f}% accuracy on {expected} clips")
    return accuracy

# Run both tests
v_acc = test_folder(VIOLENT_DIR, "violent", test_count=10)
nv_acc = test_folder(NONVIOLENT_DIR, "nonviolent", test_count=10)

print("\n" + "=" * 50)
print("  AMPLE MODEL v2 — FINAL REPORT")
print("=" * 50)
print(f"  Violent detection accuracy:     {v_acc:.1f}%")
print(f"  Non-violent detection accuracy: {nv_acc:.1f}%")
print(f"  Overall accuracy:               {((v_acc + nv_acc) / 2):.1f}%")
print("=" * 50)