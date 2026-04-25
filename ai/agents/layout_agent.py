import json
import re
import streamlit as st

from ai.llm import invoke_llm
from ai.prompts import SYSTEM_PCB_EXPERT, LAYOUT_AGENT_PROMPT


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
# 🧩 BUILD CONTEXT
# ----------------------------------------
def build_layout_context(vision=None, graph=None, ocr=None, gnn=None):

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
# 🧩 MAIN LAYOUT ANALYSIS
# ----------------------------------------
def run_layout_agent(context, structured=True):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    {LAYOUT_AGENT_PROMPT}

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
# 🔍 ADVANCED LAYOUT ANALYSIS
# ----------------------------------------
def advanced_layout_analysis(context):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    Perform deep PCB layout analysis.

    Check:
    - Component placement optimization
    - Routing efficiency
    - Layer usage
    - Signal path clarity
    - Power vs signal separation
    - EMI/EMC risk zones

    Context:
    {context}

    Output JSON:
    {{
        "placement_quality": "...",
        "routing_efficiency": "...",
        "layer_usage": "...",
        "issues": [...],
        "recommendations": [...]
    }}
    """

    response = invoke_llm(system_prompt, user_prompt)

    return extract_json(response)


# ----------------------------------------
# ⚠️ DESIGN RULE CHECK (DRC)
# ----------------------------------------
def drc_analysis(context):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    Perform Design Rule Check (DRC).

    Check:
    - Clearance violations
    - Spacing issues
    - Trace width compliance
    - Via spacing
    - Component overlap

    Context:
    {context}

    Output JSON:
    {{
        "violations": [
            {{
                "type": "...",
                "severity": "...",
                "fix": "..."
            }}
        ]
    }}
    """

    response = invoke_llm(system_prompt, user_prompt)

    return extract_json(response)


# ----------------------------------------
# 🏭 MANUFACTURABILITY (DFM)
# ----------------------------------------
def manufacturability_analysis(context):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    Evaluate manufacturability (DFM).

    Check:
    - Minimum trace width
    - Drill size feasibility
    - Solder mask issues
    - Component accessibility
    - Assembly complexity

    Context:
    {context}

    Output JSON:
    {{
        "dfm_score": "...",
        "issues": [...],
        "recommendations": [...]
    }}
    """

    response = invoke_llm(system_prompt, user_prompt)

    return extract_json(response)


# ----------------------------------------
# 📊 LAYOUT SCORE
# ----------------------------------------
def layout_score(context):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    Evaluate PCB layout quality.

    Context:
    {context}

    Provide:
    - score (0-100)
    - explanation
    """

    response = invoke_llm(system_prompt, user_prompt)

    return extract_json(response)


# ----------------------------------------
# ⚡ QUICK LAYOUT CHECK
# ----------------------------------------
def quick_layout_check(context):

    system_prompt = "You are a PCB layout expert."

    user_prompt = f"""
    Quickly identify layout issues:

    {context}

    Output short bullet points.
    """

    return invoke_llm(system_prompt, user_prompt)


# ----------------------------------------
# 🔄 STREAMLIT CACHED VERSION
# ----------------------------------------
@st.cache_data(show_spinner=False)
def cached_layout_agent(context):
    return run_layout_agent(context)


# ----------------------------------------
# 🧠 PRIORITIZE LAYOUT ISSUES
# ----------------------------------------
def prioritize_layout_issues(layout_output):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    Prioritize layout issues:

    {layout_output}

    Rank based on severity and impact.
    """

    return invoke_llm(system_prompt, user_prompt)


# ----------------------------------------
# 🔧 LAYOUT OPTIMIZATION SUGGESTIONS
# ----------------------------------------
def layout_optimization(context):

    system_prompt = SYSTEM_PCB_EXPERT

    user_prompt = f"""
    Suggest layout optimizations.

    Context:
    {context}

    Recommend:
    - Component repositioning
    - Routing improvements
    - Layer restructuring
    - EMI reduction strategies
    """

    return invoke_llm(system_prompt, user_prompt)
