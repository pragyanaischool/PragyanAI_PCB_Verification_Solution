import json
import re
import streamlit as st

from ai.llm import invoke_llm
from ai.prompts import SYSTEM_PCB_EXPERT, THERMAL_AGENT_PROMPT


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
# 🌡️ BUILD CONTEXT
# ----------------------------------------
def build_thermal_context(vision=None, graph=None, ocr=None, gnn=None):

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
# 🌡️ MAIN THERMAL ANALYSIS
# ----------------------------------------
def run_thermal_agent(context, structured=True):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    {THERMAL_AGENT_PROMPT}

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
# 🔥 ADVANCED THERMAL ANALYSIS
# ----------------------------------------
def advanced_thermal_analysis(context):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    Perform deep thermal analysis.

    Check:
    - Heat concentration zones
    - Power component clustering
    - Cooling inefficiencies
    - Copper area for heat spreading
    - Thermal vias presence
    - Airflow considerations

    Context:
    {context}

    Output JSON:
    {{
        "hotspots": "...",
        "cooling_efficiency": "...",
        "heat_distribution": "...",
        "issues": [...],
        "recommendations": [...]
    }}
    """

    response = invoke_llm(system_prompt, user_prompt)

    return extract_json(response)


# ----------------------------------------
# 🌡️ THERMAL SCORE
# ----------------------------------------
def thermal_score(context):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    Evaluate thermal performance of PCB.

    Context:
    {context}

    Provide:
    - score (0-100)
    - explanation
    """

    response = invoke_llm(system_prompt, user_prompt)

    return extract_json(response)


# ----------------------------------------
# ⚡ QUICK THERMAL CHECK
# ----------------------------------------
def quick_thermal_check(context):

    system_prompt = "You are a PCB thermal expert."

    user_prompt = f"""
    Quickly identify thermal risks:

    {context}

    Output short bullet points.
    """

    return invoke_llm(system_prompt, user_prompt)


# ----------------------------------------
# 🔥 HOTSPOT DETECTION MODE
# ----------------------------------------
def hotspot_analysis(context):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    Identify thermal hotspots.

    Focus on:
    - Voltage regulators
    - Power ICs
    - Dense routing areas

    Context:
    {context}

    Output JSON:
    {{
        "hotspots": [
            {{
                "location": "...",
                "severity": "...",
                "reason": "...",
                "fix": "..."
            }}
        ]
    }}
    """

    response = invoke_llm(system_prompt, user_prompt)

    return extract_json(response)


# ----------------------------------------
# 🔄 STREAMLIT CACHED VERSION
# ----------------------------------------
@st.cache_data(show_spinner=False)
def cached_thermal_agent(context):
    return run_thermal_agent(context)


# ----------------------------------------
# 🧠 PRIORITIZE THERMAL ISSUES
# ----------------------------------------
def prioritize_thermal_issues(thermal_output):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    Prioritize thermal issues:

    {thermal_output}

    Rank based on severity and risk.
    """

    return invoke_llm(system_prompt, user_prompt)


# ----------------------------------------
# 🌬️ COOLING STRATEGY SUGGESTION
# ----------------------------------------
def cooling_strategy(context):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    Suggest cooling improvements.

    Context:
    {context}

    Recommend:
    - Heat sinks
    - Thermal vias
    - Copper pours
    - Airflow design
    """

    return invoke_llm(system_prompt, user_prompt)
