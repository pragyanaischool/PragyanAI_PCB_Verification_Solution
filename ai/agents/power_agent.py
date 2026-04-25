import json
import re
import streamlit as st

from ai.llm import invoke_llm
from ai.prompts import SYSTEM_PCB_EXPERT, POWER_AGENT_PROMPT


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
# ⚡ BUILD CONTEXT
# ----------------------------------------
def build_power_context(vision=None, graph=None, ocr=None, gnn=None):

    return f"""
    PCB CONTEXT:

    Vision Analysis:
    {vision}

    Graph Summary:
    {graph}

    OCR Data:
    {ocr}

    GNN Output:
    {gnn}
    """


# ----------------------------------------
# ⚡ MAIN POWER ANALYSIS
# ----------------------------------------
def run_power_agent(context, structured=True):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    {POWER_AGENT_PROMPT}

    Context:
    {context}

    {"Return structured JSON." if structured else ""}
    
    Format:
    {{
        "issues": [
            {{
                "issue": "...",
                "severity": "High/Medium/Low",
                "explanation": "...",
                "fix": "..."
            }}
        ],
        "summary": "..."
    }}
    """

    response = invoke_llm(system_prompt, user_prompt)

    if structured:
        return extract_json(response)

    return response


# ----------------------------------------
# 🔍 ADVANCED POWER ANALYSIS (DETAILED)
# ----------------------------------------
def advanced_power_analysis(context):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    Perform deep power integrity analysis.

    Check:
    - Ground plane continuity
    - Voltage stability
    - Current distribution
    - Decoupling capacitor placement
    - Power trace width
    - Return paths

    Context:
    {context}

    Output JSON:
    {{
        "power_distribution": "...",
        "grounding": "...",
        "decoupling": "...",
        "issues": [...],
        "recommendations": [...]
    }}
    """

    response = invoke_llm(system_prompt, user_prompt)

    return extract_json(response)


# ----------------------------------------
# 📊 POWER SCORING
# ----------------------------------------
def power_score(context):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    Evaluate power integrity.

    Context:
    {context}

    Give:
    - score (0-100)
    - explanation
    """

    response = invoke_llm(system_prompt, user_prompt)

    return extract_json(response)


# ----------------------------------------
# ⚡ QUICK POWER CHECK (FAST)
# ----------------------------------------
def quick_power_check(context):

    system_prompt = "You are a PCB power expert."

    user_prompt = f"""
    Quickly identify major power issues:

    {context}

    Return short bullet points.
    """

    return invoke_llm(system_prompt, user_prompt)


# ----------------------------------------
# 🔄 STREAMLIT CACHED VERSION
# ----------------------------------------
@st.cache_data(show_spinner=False)
def cached_power_agent(context):
    return run_power_agent(context)


# ----------------------------------------
# 🧠 ISSUE PRIORITIZATION
# ----------------------------------------
def prioritize_power_issues(power_output):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    Prioritize these power issues:

    {power_output}

    Sort by severity and impact.
    """

    return invoke_llm(system_prompt, user_prompt)
