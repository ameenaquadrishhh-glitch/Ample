import os
import cv2
import shutil

# Paths to your downloaded dataset
VIOLENT_DIR = "./A-Dataset-for-Automatic-Violence-Detection-in-Videos/violence-detection-dataset/violent/cam1"
NONVIOLENT_DIR = "./A-Dataset-for-Automatic-Violence-Detection-in-Videos/violence-detection-dataset/non-violent/cam1"

# Output folder
OUTPUT_DIR = "./dataset/images"
os.makedirs(f"{OUTPUT_DIR}/train/violent", exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/train/nonviolent", exist_ok=True)

def extract_frames(video_folder, label, max_videos=50, frames_per_video=10):
    videos = [f for f in os.listdir(video_folder) if f.endswith('.mp4')][:max_videos]
    count = 0
    for video_name in videos:
        cap = cv2.VideoCapture(os.path.join(video_folder, video_name))
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        step = max(1, total // frames_per_video)
        frame_num = 0
        saved = 0
        while saved < frames_per_video:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = cap.read()
            if not ret:
                break
            filename = f"{OUTPUT_DIR}/train/{label}/{label}_{count}.jpg"
            cv2.imwrite(filename, frame)
            count += 1
            saved += 1
            frame_num += step
        cap.release()
    print(f"Extracted {count} frames for {label}")

extract_frames(VIOLENT_DIR, "violent")
extract_frames(NONVIOLENT_DIR, "nonviolent")
print("Dataset preparation complete!")