import os
import re
from typing import Dict, List

# Optional imports
try:
    import pytesseract
    import cv2
    import numpy as np
    from PIL import Image
except:
    pytesseract = None
    cv2 = None


# ----------------------------------------
# 🧠 MAIN IMAGE PARSER (SAFE + DEBUG)
# ----------------------------------------
def parse_from_image(image_path: str) -> Dict:

    debug_info = {}

    # ----------------------------------------
    # 🔍 FILE VALIDATION
    # ----------------------------------------
    if not os.path.exists(image_path):
        return {
            "components": [],
            "nets": [],
            "error": f"File does not exist: {image_path}"
        }

    file_size = os.path.getsize(image_path)
    debug_info["file_size_bytes"] = file_size

    if file_size == 0:
        return {
            "components": [],
            "nets": [],
            "error": f"File is empty: {image_path}"
        }

    # ----------------------------------------
    # 🖼️ LOAD IMAGE (OpenCV)
    # ----------------------------------------
    img = None

    if cv2:
        img = cv2.imread(image_path)

    # ----------------------------------------
    # 🔁 FALLBACK → PIL
    # ----------------------------------------
    if img is None:
        try:
            pil_img = Image.open(image_path).convert("RGB")
            img = np.array(pil_img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            debug_info["fallback"] = "PIL used"
        except Exception as e:
            return {
                "components": [],
                "nets": [],
                "error": f"Image loading failed (OpenCV + PIL): {str(e)}",
                "debug": debug_info
            }

    # ----------------------------------------
    # 🚨 FINAL CHECK
    # ----------------------------------------
    if img is None:
        return {
            "components": [],
            "nets": [],
            "error": f"Failed to load image: {image_path}",
            "debug": debug_info
        }

    debug_info["image_shape"] = str(img.shape)

    # ----------------------------------------
    # 🎯 CONVERT TO GRAYSCALE
    # ----------------------------------------
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except Exception as e:
        return {
            "components": [],
            "nets": [],
            "error": f"cvtColor failed: {str(e)}",
            "debug": debug_info
        }

    # ----------------------------------------
    # 🔤 OCR (OPTIONAL)
    # ----------------------------------------
    text = ""

    if pytesseract:
        try:
            text = pytesseract.image_to_string(gray)
            debug_info["ocr_length"] = len(text)
        except Exception as e:
            debug_info["ocr_error"] = str(e)
    else:
        debug_info["ocr"] = "pytesseract not installed"

    # ----------------------------------------
    # 🔍 COMPONENT EXTRACTION
    # ----------------------------------------
    components = extract_components_from_text(text)

    # ----------------------------------------
    # 🔗 BUILD DUMMY NETS
    # ----------------------------------------
    nets = build_dummy_nets(components)

    # ----------------------------------------
    # 📦 FINAL OUTPUT
    # ----------------------------------------
    return {
        "components": components,
        "nets": nets,
        "raw_text": text,
        "debug": debug_info
    }


# ----------------------------------------
# 🔍 TEXT → COMPONENT EXTRACTION
# ----------------------------------------
def extract_components_from_text(text: str) -> List[str]:

    pattern = r"\b(U\d+|R\d+|C\d+|L\d+|D\d+|Q\d+)\b"
    components = re.findall(pattern, text)

    return list(set(components))


# ----------------------------------------
# 🔗 DUMMY NET BUILDER
# ----------------------------------------
def build_dummy_nets(components: List[str]):

    nets = []

    for i in range(len(components) - 1):
        nets.append((components[i], components[i + 1]))

    return nets
