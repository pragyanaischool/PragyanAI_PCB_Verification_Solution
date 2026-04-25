"""
PCB Parser Service (NO OpenCV VERSION)

- Uses PIL only (safe for Streamlit Cloud)
- OCR supported (pytesseract)
- Debug-friendly
- Import-safe
"""

import os
import re
from typing import Dict, List

# Safe imports
try:
    from PIL import Image
    import pytesseract
except Exception:
    Image = None
    pytesseract = None


# ----------------------------------------
# 🧠 MAIN ENTRY
# ----------------------------------------
def parse_pcb(file_path: str) -> Dict:
    """
    Main parser entry point
    """

    if not file_path:
        return {"error": "Empty file path"}

    if not os.path.exists(file_path):
        return {"error": f"File does not exist: {file_path}"}

    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".png", ".jpg", ".jpeg"]:
        return parse_from_image(file_path)

    elif ext in [".txt", ".net", ".netlist"]:
        return parse_netlist(file_path)

    return {
        "components": [],
        "nets": [],
        "error": f"Unsupported file format: {ext}"
    }


# ----------------------------------------
# 🖼️ IMAGE PARSER (PIL ONLY)
# ----------------------------------------
def parse_from_image(image_path: str) -> Dict:

    debug = {}

    # Validate file
    if not os.path.exists(image_path):
        return {"error": f"File not found: {image_path}"}

    file_size = os.path.getsize(image_path)
    debug["file_size"] = file_size

    if file_size == 0:
        return {"error": "File is empty", "debug": debug}

    # Load image with PIL
    try:
        img = Image.open(image_path).convert("RGB")
        debug["image_mode"] = img.mode
        debug["image_size"] = img.size
    except Exception as e:
        return {
            "error": f"Failed to load image using PIL: {str(e)}",
            "debug": debug
        }

    # Convert to grayscale (for OCR)
    try:
        gray = img.convert("L")
    except Exception as e:
        return {
            "error": f"Grayscale conversion failed: {str(e)}",
            "debug": debug
        }

    # OCR
    text = ""
    if pytesseract:
        try:
            text = pytesseract.image_to_string(gray)
            debug["ocr_length"] = len(text)
        except Exception as e:
            debug["ocr_error"] = str(e)
    else:
        debug["ocr"] = "pytesseract not installed"

    # Extract components
    components = extract_components_from_text(text)

    # Build dummy nets
    nets = build_dummy_nets(components)

    return {
        "components": components,
        "nets": nets,
        "raw_text": text,
        "debug": debug
    }


# ----------------------------------------
# 📜 NETLIST PARSER
# ----------------------------------------
def parse_netlist(file_path: str) -> Dict:

    components = set()
    nets = []

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception as e:
        return {"error": f"Failed to read netlist: {str(e)}"}

    for line in lines:
        tokens = re.findall(r"\b[A-Z]+\d+\b", line)

        if len(tokens) >= 2:
            components.update(tokens)
            nets.append((tokens[0], tokens[1]))

    return {
        "components": list(components),
        "nets": nets
    }


# ----------------------------------------
# 🔍 COMPONENT EXTRACTION
# ----------------------------------------
def extract_components_from_text(text: str) -> List[str]:

    pattern = r"\b(U\d+|R\d+|C\d+|L\d+|D\d+|Q\d+)\b"
    return list(set(re.findall(pattern, text)))


# ----------------------------------------
# 🔗 DUMMY NET BUILDER
# ----------------------------------------
def build_dummy_nets(components: List[str]):

    nets = []

    for i in range(len(components) - 1):
        nets.append((components[i], components[i + 1]))

    return nets
