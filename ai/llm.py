import streamlit as st
from langchain_groq import ChatGroq
#from langchain.schema import HumanMessage, SystemMessage
from langchain_core.messages import HumanMessage, SystemMessage
import json
import re

# -----------------------------
# 🔐 LOAD LLM (CACHED)
# -----------------------------
@st.cache_resource
def get_llm():
    return ChatGroq(
        model_name="llama3-70b-8192",
        temperature=0.2,
        groq_api_key=st.secrets["GROQ_API_KEY"]
    )

# -----------------------------
# 🧠 BASE INVOKE FUNCTION
# -----------------------------
def invoke_llm(system_prompt: str, user_prompt: str):

    llm = get_llm()

    try:
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])

        return response.content

    except Exception as e:
        return f"LLM Error: {str(e)}"


# -----------------------------
# 🧾 JSON PARSER (ROBUST)
# -----------------------------
def extract_json(text):

    try:
        return json.loads(text)
    except:
        # Try to extract JSON substring
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass

    return {
        "raw_output": text
    }


# -----------------------------
# 🧠 STRUCTURED ANALYSIS CALL
# -----------------------------
def structured_analysis(context: str):

    system_prompt = """
    You are an expert PCB design engineer.

    Always return structured JSON output.
    """

    user_prompt = f"""
    Analyze the PCB system:

    {context}

    Return JSON format:

    {{
        "summary": "...",
        "issues": [
            {{
                "category": "Power/Signal/Thermal/Layout",
                "issue": "...",
                "severity": "High/Medium/Low",
                "explanation": "...",
                "fix": "..."
            }}
        ],
        "score": 0-100
    }}
    """

    raw = invoke_llm(system_prompt, user_prompt)

    return extract_json(raw)


# -----------------------------
# ⚡ POWER AGENT
# -----------------------------
def power_analysis(context):

    return invoke_llm(
        "You are a PCB Power Integrity Expert.",
        f"""
        Analyze power-related issues:
        {context}

        Output:
        - issue
        - severity
        - fix
        """
    )


# -----------------------------
# 🔌 SIGNAL AGENT
# -----------------------------
def signal_analysis(context):

    return invoke_llm(
        "You are a Signal Integrity Engineer.",
        f"""
        Analyze signal routing:
        {context}

        Detect:
        - Crosstalk
        - Reflection
        - Mismatch
        """
    )


# -----------------------------
# 🌡️ THERMAL AGENT
# -----------------------------
def thermal_analysis(context):

    return invoke_llm(
        "You are a Thermal Engineer.",
        f"""
        Analyze heat risks:
        {context}

        Detect:
        - hotspots
        - poor dissipation
        """
    )


# -----------------------------
# 🧩 LAYOUT AGENT
# -----------------------------
def layout_analysis(context):

    return invoke_llm(
        "You are a PCB Layout Expert.",
        f"""
        Analyze layout issues:
        {context}

        Check:
        - spacing
        - placement
        - routing efficiency
        """
    )


# -----------------------------
# 🧠 MASTER AGENT
# -----------------------------
def run_multi_agent_analysis(context):

    return {
        "power": power_analysis(context),
        "signal": signal_analysis(context),
        "thermal": thermal_analysis(context),
        "layout": layout_analysis(context),
        "final": structured_analysis(context)
    }


# -----------------------------
# 💬 CHAT MODE (INTERACTIVE)
# -----------------------------
def chat_with_pcb(context, user_query):

    system_prompt = """
    You are a PCB AI assistant helping engineers debug and improve designs.
    """

    user_prompt = f"""
    PCB Context:
    {context}

    User Question:
    {user_query}
    """

    return invoke_llm(system_prompt, user_prompt)
