import streamlit as st
import json
import re

from ai.vlm import analyze_image, analyze_front_back
from ai.llm import invoke_llm
from ai.prompts import VISION_ANALYSIS_PROMPT


# ----------------------------------------
# 🧾 JSON PARSER (ROBUST)
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
# 👁️ RAW VISION ANALYSIS (VLM ONLY)
# ----------------------------------------
def run_vision_vlm(image_path):
    """
    Calls Hugging Face VLM directly
    """
    try:
        result = analyze_image(image_path)
        return result
    except Exception as e:
        return f"Vision Error: {str(e)}"


# ----------------------------------------
# 🧠 VISION + LLM REASONING
# ----------------------------------------
def refine_vision_with_llm(vlm_output):
    """
    Convert raw VLM output into structured insights
    """

    system_prompt = """
    You are a PCB Vision Analysis Expert.
    Convert raw vision observations into structured engineering insights.
    """

    user_prompt = f"""
    Raw Vision Output:
    {vlm_output}

    Convert into JSON:

    {{
        "routing_density": "...",
        "congestion_areas": "...",
        "power_issues": "...",
        "thermal_hotspots": "...",
        "placement_issues": "...",
        "summary": "..."
    }}
    """

    response = invoke_llm(system_prompt, user_prompt)

    return extract_json(response)


# ----------------------------------------
# 🚀 MAIN VISION AGENT (SINGLE IMAGE)
# ----------------------------------------
def run_vision_agent(image_path, use_llm_refinement=True):
    """
    Full pipeline:
    Image → VLM → (Optional) LLM refinement
    """

    # Step 1: Raw VLM
    vlm_output = run_vision_vlm(image_path)

    if not use_llm_refinement:
        return {
            "type": "vision",
            "raw": vlm_output
        }

    # Step 2: Structured reasoning
    structured = refine_vision_with_llm(vlm_output)

    return {
        "type": "vision",
        "raw": vlm_output,
        "structured": structured
    }


# ----------------------------------------
# 🔄 FRONT + BACK PCB ANALYSIS
# ----------------------------------------
def run_multilayer_vision(front_path, back_path):
    """
    Analyze both PCB layers
    """

    try:
        multi = analyze_front_back(front_path, back_path)

        combined_prompt = f"""
        Analyze combined PCB layers:

        FRONT:
        {multi['front']}

        BACK:
        {multi['back']}

        Identify:
        - Cross-layer issues
        - Via problems
        - Alignment mismatches
        - Overall board quality

        Return structured JSON.
        """

        result = invoke_llm(VISION_ANALYSIS_PROMPT, combined_prompt)

        return extract_json(result)

    except Exception as e:
        return {"error": str(e)}


# ----------------------------------------
# ⚡ CACHED VERSION (STREAMLIT)
# ----------------------------------------
@st.cache_data(show_spinner=False)
def cached_vision_agent(image_path):
    return run_vision_agent(image_path)


# ----------------------------------------
# 🎯 ADVANCED REGION-LEVEL ANALYSIS
# ----------------------------------------
def region_based_analysis(image_path):
    """
    Future-ready function:
    Divide PCB into regions and analyze separately
    """

    vlm_output = run_vision_vlm(image_path)

    prompt = f"""
    Divide PCB into regions and analyze:

    {vlm_output}

    Output:
    [
        {{
            "region": "Top Left",
            "issue": "...",
            "severity": "High/Medium/Low"
        }}
    ]
    """

    result = invoke_llm("PCB Region Analysis Expert", prompt)

    return extract_json(result)
