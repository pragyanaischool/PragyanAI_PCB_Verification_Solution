import json
import re
import streamlit as st

from ai.llm import invoke_llm
from ai.prompts import SYSTEM_PCB_EXPERT, SIGNAL_AGENT_PROMPT


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
# 🔌 BUILD CONTEXT
# ----------------------------------------
def build_signal_context(vision=None, graph=None, ocr=None, gnn=None):

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
# 🔌 MAIN SIGNAL ANALYSIS
# ----------------------------------------
def run_signal_agent(context, structured=True):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    {SIGNAL_AGENT_PROMPT}

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
# 🔍 ADVANCED SIGNAL ANALYSIS
# ----------------------------------------
def advanced_signal_analysis(context):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    Perform deep signal integrity analysis.

    Check:
    - Crosstalk between traces
    - Impedance mismatch
    - Signal reflection
    - Trace length mismatch
    - High-speed routing issues
    - Differential pair imbalance

    Context:
    {context}

    Output JSON:
    {{
        "crosstalk": "...",
        "impedance": "...",
        "reflections": "...",
        "length_matching": "...",
        "issues": [...],
        "recommendations": [...]
    }}
    """

    response = invoke_llm(system_prompt, user_prompt)

    return extract_json(response)


# ----------------------------------------
# 📊 SIGNAL QUALITY SCORE
# ----------------------------------------
def signal_score(context):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    Evaluate signal integrity quality.

    Context:
    {context}

    Provide:
    - score (0-100)
    - explanation
    """

    response = invoke_llm(system_prompt, user_prompt)

    return extract_json(response)


# ----------------------------------------
# ⚡ QUICK SIGNAL CHECK
# ----------------------------------------
def quick_signal_check(context):

    system_prompt = "You are a PCB signal integrity expert."

    user_prompt = f"""
    Quickly identify major signal issues:

    {context}

    Output short bullet points.
    """

    return invoke_llm(system_prompt, user_prompt)


# ----------------------------------------
# 🔄 STREAMLIT CACHED VERSION
# ----------------------------------------
@st.cache_data(show_spinner=False)
def cached_signal_agent(context):
    return run_signal_agent(context)


# ----------------------------------------
# 🧠 PRIORITIZE SIGNAL ISSUES
# ----------------------------------------
def prioritize_signal_issues(signal_output):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    Prioritize signal integrity issues:

    {signal_output}

    Rank by severity and impact.
    """

    return invoke_llm(system_prompt, user_prompt)


# ----------------------------------------
# 🔬 HIGH-SPEED ANALYSIS MODE
# ----------------------------------------
def high_speed_signal_analysis(context):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    Analyze PCB for high-speed signal issues.

    Focus on:
    - Transmission line effects
    - Differential pairs
    - EMI/EMC risks
    - Clock signal integrity

    Context:
    {context}

    Output structured JSON.
    """

    response = invoke_llm(system_prompt, user_prompt)

    return extract_json(response)
