import requests
import streamlit as st
import base64
import time
import json
import re
from typing import Optional, Dict


# ----------------------------------------
# 🔐 CONFIG
# ----------------------------------------
HF_API_TOKEN = st.secrets.get("HF_API_TOKEN", "")
HF_API_URL = st.secrets.get("HF_API_URL", "")  # optional (Space API)

# Default → LLaVA model endpoint
DEFAULT_MODEL_URL = "https://api-inference.huggingface.co/models/llava-hf/llava-1.5-7b-hf"

HEADERS = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
} if HF_API_TOKEN else {}


# ----------------------------------------
# 🧠 IMAGE → BASE64
# ----------------------------------------
def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# ----------------------------------------
# 🧾 RESPONSE PARSER
# ----------------------------------------
def parse_response(res):

    try:
        if isinstance(res, list):
            return res[0].get("generated_text", str(res))

        if isinstance(res, dict):
            return res.get("generated_text", str(res))

        return str(res)

    except Exception:
        return str(res)


# ----------------------------------------
# 🔄 JSON EXTRACTION (OPTIONAL)
# ----------------------------------------
def extract_json(text):

    try:
        return json.loads(text)
    except:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass

    return {"raw_output": text}


# ----------------------------------------
# 🚀 CORE API CALL (GENERIC)
# ----------------------------------------
def call_hf_api(url: str, payload: Dict, retries=3, wait=5):

    for attempt in range(retries):

        try:
            response = requests.post(
                url,
                headers=HEADERS,
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                return parse_response(response.json())

            # Model loading case
            if "loading" in response.text.lower():
                time.sleep(wait)
                continue

            return f"Error {response.status_code}: {response.text}"

        except Exception as e:
            if attempt < retries - 1:
                time.sleep(wait)
            else:
                return f"Exception: {str(e)}"


# ----------------------------------------
# 👁️ MAIN ANALYSIS (AUTO SELECT)
# ----------------------------------------
def analyze_image(image_path: str, prompt: Optional[str] = None):

    if prompt is None:
        prompt = DEFAULT_PROMPT()

    # Prefer Space API if provided
    if HF_API_URL:
        return call_space_api(image_path, prompt)

    # Else fallback to LLaVA API
    return call_llava_api(image_path, prompt)


# ----------------------------------------
# 🧠 DEFAULT PROMPT
# ----------------------------------------
def DEFAULT_PROMPT():

    return """
    You are a PCB design expert.

    Analyze this PCB image and identify:

    - Routing density
    - Trace congestion
    - Signal integrity issues
    - Power distribution problems
    - Thermal hotspots
    - Component placement issues

    Provide detailed technical observations.
    """


# ----------------------------------------
# 🚀 LLaVA API CALL
# ----------------------------------------
def call_llava_api(image_path: str, prompt: str):

    image_b64 = encode_image(image_path)

    payload = {
        "inputs": {
            "image": image_b64,
            "text": prompt
        }
    }

    return call_hf_api(DEFAULT_MODEL_URL, payload)


# ----------------------------------------
# 🚀 HF SPACE API CALL (OPTIONAL)
# ----------------------------------------
def call_space_api(image_path: str, prompt: str):

    with open(image_path, "rb") as f:
        files = {"data": f}

        response = requests.post(
            HF_API_URL,
            headers=HEADERS,
            files=files,
            timeout=60
        )

    if response.status_code != 200:
        return f"Space Error: {response.text}"

    try:
        data = response.json()

        if "data" in data:
            return data["data"][0]

        return str(data)

    except:
        return response.text


# ----------------------------------------
# 🔄 MULTI-IMAGE (FRONT + BACK)
# ----------------------------------------
def analyze_front_back(front_path: str, back_path: str):

    front = analyze_image(front_path)
    back = analyze_image(back_path)

    combined = f"""
    FRONT ANALYSIS:
    {front}

    BACK ANALYSIS:
    {back}

    Identify:
    - Cross-layer issues
    - Alignment problems
    - Via issues
    - Overall PCB quality
    """

    return {
        "front": front,
        "back": back,
        "combined": combined
    }


# ----------------------------------------
# ⚡ CACHED VERSION (STREAMLIT)
# ----------------------------------------
@st.cache_data(show_spinner=False)
def cached_vlm(image_path: str):
    return analyze_image(image_path)


# ----------------------------------------
# 🎯 STRUCTURED OUTPUT WRAPPER
# ----------------------------------------
def structured_vlm_analysis(image_path: str):

    raw = analyze_image(image_path)

    structured_prompt = f"""
    Convert this into structured JSON:

    {raw}

    Format:
    {{
        "issues": [
            {{
                "type": "...",
                "severity": "High/Medium/Low",
                "description": "...",
                "region": "..."
            }}
        ],
        "summary": "..."
    }}
    """

    return {
        "raw": raw,
        "structured_prompt": structured_prompt
    }
    
