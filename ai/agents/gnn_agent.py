import json
import re
import streamlit as st

from ai.llm import invoke_llm
from ai.prompts import SYSTEM_PCB_EXPERT, GNN_PROMPT


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
# 🧠 BUILD CONTEXT
# ----------------------------------------
def build_gnn_context(graph_summary=None, gnn_output=None, vision=None, ocr=None):

    return f"""
    PCB CONTEXT:

    Graph Summary:
    {graph_summary}

    GNN Output:
    {gnn_output}

    Vision Analysis:
    {vision}

    OCR Data:
    {ocr}
    """


# ----------------------------------------
# 🤖 MAIN GNN INTERPRETATION
# ----------------------------------------
def run_gnn_agent(graph_summary, gnn_output, structured=True):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    {GNN_PROMPT}

    Graph:
    {graph_summary}

    Model Output:
    {gnn_output}

    {"Return structured JSON." if structured else ""}

    Format:
    {{
        "detected_issue": "...",
        "severity": "High/Medium/Low",
        "explanation": "...",
        "impact": "...",
        "fix": "..."
    }}
    """

    response = invoke_llm(system_prompt, user_prompt)

    if structured:
        return extract_json(response)

    return response


# ----------------------------------------
# 🔍 ADVANCED GNN ANALYSIS
# ----------------------------------------
def advanced_gnn_analysis(context):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    Perform advanced analysis using GNN predictions.

    Identify:
    - Hidden structural issues
    - Graph connectivity anomalies
    - Routing inefficiencies
    - Potential failure points

    Context:
    {context}

    Output JSON:
    {{
        "anomalies": "...",
        "connectivity_issues": "...",
        "risk_level": "...",
        "issues": [...],
        "recommendations": [...]
    }}
    """

    response = invoke_llm(system_prompt, user_prompt)

    return extract_json(response)


# ----------------------------------------
# ⚠️ ANOMALY DETECTION MODE
# ----------------------------------------
def anomaly_detection(context):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    Detect anomalies in PCB graph.

    Context:
    {context}

    Identify:
    - Unusual connections
    - Missing links
    - Overconnected nodes

    Output JSON:
    {{
        "anomalies": [
            {{
                "node": "...",
                "issue": "...",
                "severity": "...",
                "fix": "..."
            }}
        ]
    }}
    """

    response = invoke_llm(system_prompt, user_prompt)

    return extract_json(response)


# ----------------------------------------
# 📊 GNN SCORE
# ----------------------------------------
def gnn_score(context):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    Evaluate PCB graph quality.

    Context:
    {context}

    Provide:
    - score (0-100)
    - explanation
    """

    response = invoke_llm(system_prompt, user_prompt)

    return extract_json(response)


# ----------------------------------------
# ⚡ QUICK GNN CHECK
# ----------------------------------------
def quick_gnn_check(context):

    system_prompt = "You are a graph-based PCB analysis expert."

    user_prompt = f"""
    Quickly identify major graph-based issues:

    {context}

    Output short bullet points.
    """

    return invoke_llm(system_prompt, user_prompt)


# ----------------------------------------
# 🔄 STREAMLIT CACHED VERSION
# ----------------------------------------
@st.cache_data(show_spinner=False)
def cached_gnn_agent(graph_summary, gnn_output):
    return run_gnn_agent(graph_summary, gnn_output)


# ----------------------------------------
# 🧠 PRIORITIZE GNN ISSUES
# ----------------------------------------
def prioritize_gnn_issues(gnn_output):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    Prioritize GNN-detected issues:

    {gnn_output}

    Rank based on risk and severity.
    """

    return invoke_llm(system_prompt, user_prompt)


# ----------------------------------------
# 🔧 OPTIMIZATION SUGGESTIONS
# ----------------------------------------
def gnn_optimization(context):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    Suggest graph-based optimizations.

    Context:
    {context}

    Recommend:
    - Better routing structure
    - Improved connectivity
    - Reduced complexity
    """

    return invoke_llm(system_prompt, user_prompt)
