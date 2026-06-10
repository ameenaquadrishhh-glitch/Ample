from ultralytics import YOLO

model = YOLO("yolov8s-cls.pt")  # Upgraded from n to s

model.train(
    data="./dataset/images/train",
    epochs=50,
    imgsz=224,
    batch=16,
    device=0,
    workers=0,
    project="./runs",
    name="ample_v2",
    exist_ok=True,
    verbose=True
)

print("Training complete!")
print("Model saved to: ./runs/classify/ample_v2/weights/best.pt")