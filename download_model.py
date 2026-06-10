import urllib.request
import os

os.makedirs("./models", exist_ok=True)

url = "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt"
print("Downloading base model...")
urllib.request.urlretrieve(url, "./models/best.pt")
print("✅ Done! Model saved to ./models/best.pt")