"""
PCB Parser Service

Supports:
- Image-based PCB (via OCR fallback)
- Simple netlist parsing
- Extensible for KiCad / Gerber

NOTE:
This is a hybrid parser (MVP + extensible for production)
"""

import os
import re
from typing import Dict, List

# Optional OCR (used if image input)
try:
    import pytesseract
    import cv2
except:
    pytesseract = None
    cv2 = None


# ----------------------------------------
# 🧠 MAIN PARSER ENTRY
# ----------------------------------------
def parse_pcb(file_path: str) -> Dict:

    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".png", ".jpg", ".jpeg"]:
        return parse_from_image(file_path)

    elif ext in [".txt", ".net", ".netlist"]:
        return parse_netlist(file_path)

    else:
        return fallback_parser(file_path)


# ----------------------------------------
# 🖼️ IMAGE PARSER (OCR BASED)
# ----------------------------------------
def parse_from_image(image_path: str) -> Dict:

    if not pytesseract or not cv2:
        return {
            "components": [],
            "nets": [],
            "error": "OCR not available"
        }

    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray)

    components = extract_components_from_text(text)

    return {
        "components": components,
        "nets": build_dummy_nets(components),
        "raw_text": text
    }


# ----------------------------------------
# 📜 NETLIST PARSER
# ----------------------------------------
def parse_netlist(file_path: str) -> Dict:

    components = set()
    nets = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    for line in lines:

        # Extract components like R1, C2, U3
        tokens = re.findall(r"\b[A-Z]+\d+\b", line)

        if len(tokens) >= 2:
            components.update(tokens)
            nets.append((tokens[0], tokens[1]))

    return {
        "components": list(components),
        "nets": nets
    }


# ----------------------------------------
# 🔄 FALLBACK PARSER
# ----------------------------------------
def fallback_parser(file_path: str) -> Dict:

    return {
        "components": [],
        "nets": [],
        "warning": "Unsupported format"
    }


# ----------------------------------------
# 🔍 TEXT → COMPONENT EXTRACTION
# ----------------------------------------
def extract_components_from_text(text: str) -> List[str]:

    # Common PCB prefixes
    pattern = r"\b(U\d+|R\d+|C\d+|L\d+|D\d+|Q\d+)\b"

    components = re.findall(pattern, text)

    return list(set(components))


# ----------------------------------------
# 🔗 DUMMY NET GENERATOR
# ----------------------------------------
def build_dummy_nets(components: List[str]):

    nets = []

    for i in range(len(components) - 1):
        nets.append((components[i], components[i + 1]))

    return nets


# ----------------------------------------
# 🧠 ADVANCED PARSER (EXTENSION POINT)
# ----------------------------------------
def parse_kicad(file_path: str) -> Dict:
    """
    Future: integrate KiCad parser
    """
    return {
        "components": [],
        "nets": [],
        "note": "KiCad parser not implemented yet"
    }


def parse_gerber(file_path: str) -> Dict:
    """
    Future: integrate Gerber parser
    """
    return {
        "components": [],
        "nets": [],
        "note": "Gerber parser not implemented yet"
    }
