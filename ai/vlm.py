import requests
import streamlit as st
import base64
import json
import time

# ----------------------------------------
# 🔐 CONFIG
# ----------------------------------------
HF_API_URL = st.secrets.get("HF_API_URL", "")
HF_API_TOKEN = st.secrets.get("HF_API_TOKEN", None)

HEADERS = {}
if HF_API_TOKEN:
    HEADERS["Authorization"] = f"Bearer {HF_API_TOKEN}"


# ----------------------------------------
# 🧠 HELPER: IMAGE → BASE64
# ----------------------------------------
def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# ----------------------------------------
# 🧾 PARSE RESPONSE (ROBUST)
# ----------------------------------------
def parse_vlm_output(response_json):
    try:
        # HF Spaces (Gradio) usually returns {"data": ["text output"]}
        if isinstance(response_json, dict) and "data" in response_json:
            return response_json["data"][0]

        # Direct model response
        if isinstance(response_json, list):
            return response_json[0].get("generated_text", str(response_json))

        return str(response_json)

    except Exception:
        return str(response_json)


# ----------------------------------------
# 🚀 CORE VLM CALL
# ----------------------------------------
def call_vlm_api(image_bytes, prompt):

    payload = {
        "inputs": {
            "image": base64.b64encode(image_bytes).decode("utf-8"),
            "prompt": prompt
        }
    }

    try:
        response = requests.post(
            HF_API_URL,
            headers=HEADERS,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            return f"VLM API Error: {response.text}"

        return parse_vlm_output(response.json())

    except requests.exceptions.Timeout:
        return "VLM Timeout Error"
    except Exception as e:
        return f"VLM Exception: {str(e)}"


# ----------------------------------------
# 👁️ MAIN ANALYSIS FUNCTION
# ----------------------------------------
def analyze_image(image_path):

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    prompt = """
    You are an expert PCB design analyst.

    Analyze this PCB image and provide:
    - Dense routing regions
    - Trace congestion
    - Possible signal issues
    - Power distribution concerns
    - Thermal hotspots
    - Component placement anomalies

    Output in structured bullet points.
    """

    return call_vlm_api(image_bytes, prompt)


# ----------------------------------------
# 🔄 MULTI-IMAGE (FRONT + BACK)
# ----------------------------------------
def analyze_front_back(front_path, back_path):

    front = analyze_image(front_path)
    back = analyze_image(back_path)

    combined_prompt = f"""
    You are a PCB expert.

    FRONT ANALYSIS:
    {front}

    BACK ANALYSIS:
    {back}

    Combine insights:
    - Cross-layer issues
    - Alignment problems
    - Through-hole/via concerns
    - Overall board health
    """

    # Reuse LLM if needed later
    return {
        "front": front,
        "back": back,
        "combined": combined_prompt
    }


# ----------------------------------------
# ⚡ CACHED VERSION (STREAMLIT)
# ----------------------------------------
@st.cache_data(show_spinner=False)
def cached_vlm(image_path):
    return analyze_image(image_path)


# ----------------------------------------
# 🎯 ADVANCED STRUCTURED OUTPUT
# ----------------------------------------
def structured_vlm_analysis(image_path):

    raw = analyze_image(image_path)

    prompt = f"""
    Convert this PCB vision analysis into structured JSON:

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

    # You can pass this to LLM later
    return {
        "raw": raw,
        "structured_prompt": prompt
    }
  
