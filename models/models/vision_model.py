#Image → detections (components, traces)
import cv2
import numpy as np

def extract_features(image_path):

    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect edges (traces)
    edges = cv2.Canny(gray, 50, 150)

    # Detect blobs (components approximation)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    components = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        if w*h > 500:  # filter noise
            components.append({
                "bbox": (x, y, w, h),
                "center": (x+w//2, y+h//2)
            })

    return {
        "components": components,
        "edges": edges
    }
