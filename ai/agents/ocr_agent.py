import json
import re
import streamlit as st

from ai.llm import invoke_llm
from ai.prompts import SYSTEM_PCB_EXPERT, OCR_PROMPT


# ----------------------------------------
# 🧾 JSON PARSER
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
# 📜 BUILD CONTEXT
# ----------------------------------------
def build_ocr_context(ocr_text, vision=None, graph=None):

    return f"""
    PCB CONTEXT:

    OCR TEXT:
    {ocr_text}

    Vision:
    {vision}

    Graph:
    {graph}
    """


# ----------------------------------------
# 🔤 MAIN OCR ANALYSIS
# ----------------------------------------
def run_ocr_agent(ocr_text, structured=True):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    {OCR_PROMPT}

    OCR DATA:
    {ocr_text}

    {"Return structured JSON." if structured else ""}

    Format:
    {{
        "components": [
            {{
                "name": "...",
                "type": "Resistor/Capacitor/IC",
                "value": "...",
                "role": "..."
            }}
        ],
        "power_labels": ["5V", "GND"],
        "important_ic": ["..."],
        "summary": "..."
    }}
    """

    response = invoke_llm(system_prompt, user_prompt)

    if structured:
        return extract_json(response)

    return response


# ----------------------------------------
# 🔍 ADVANCED OCR ANALYSIS
# ----------------------------------------
def advanced_ocr_analysis(context):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    Perform deep OCR interpretation.

    Context:
    {context}

    Identify:
    - Circuit type
    - Power domains
    - Key IC roles
    - Signal flow hints

    Output JSON.
    """

    response = invoke_llm(system_prompt, user_prompt)

    return extract_json(response)


# ----------------------------------------
# ⚡ QUICK OCR CHECK
# ----------------------------------------
def quick_ocr_check(ocr_text):

    return invoke_llm(
        "You are a PCB text analysis expert.",
        f"Summarize OCR data:\n{ocr_text}"
    )


# ----------------------------------------
# 🔄 CACHE
# ----------------------------------------
@st.cache_data(show_spinner=False)
def cached_ocr_agent(ocr_text):
    return run_ocr_agent(ocr_text)
