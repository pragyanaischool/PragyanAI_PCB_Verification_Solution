from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def detect_components(image_path):

    results = model(image_path)

    comps = []

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            x1, y1, x2, y2 = box.xyxy[0]

            comps.append({
                "type": model.names[cls],
                "center": [(x1+x2)/2, (y1+y2)/2]
            })

    return comps
