import streamlit as st

# Agents
from ai.agents.vision_agent import run_vision_agent
from ai.agents.power_agent import run_power_agent
from ai.agents.signal_agent import run_signal_agent
from ai.agents.thermal_agent import run_thermal_agent
from ai.agents.layout_agent import run_layout_agent
from ai.agents.gnn_agent import run_gnn_agent
from ai.agents.ocr_agent import run_ocr_agent

from ai.llm import structured_analysis


# ----------------------------------------
# 🧠 BUILD CONTEXT
# ----------------------------------------
def build_context(vision, graph, ocr, gnn):

    return f"""
    PCB CONTEXT:

    Vision Analysis:
    {vision}

    Graph Summary:
    {graph}

    OCR Analysis:
    {ocr}

    GNN Output:
    {gnn}
    """


# ----------------------------------------
# 🚀 MAIN ORCHESTRATOR
# ----------------------------------------
def run_full_analysis(image_path, graph_summary, gnn_output, ocr_text):

    # Step 1: Vision
    vision_result = run_vision_agent(image_path)

    # Step 2: OCR
    ocr_result = run_ocr_agent(ocr_text)

    # Step 3: Context
    context = build_context(
        vision=vision_result,
        graph=graph_summary,
        ocr=ocr_result,
        gnn=gnn_output
    )

    # Step 4: Domain Agents
    power = run_power_agent(context)
    signal = run_signal_agent(context)
    thermal = run_thermal_agent(context)
    layout = run_layout_agent(context)
    gnn = run_gnn_agent(graph_summary, gnn_output)

    # Step 5: Final Consolidation
    final_report = structured_analysis(context)

    return {
        "vision": vision_result,
        "ocr": ocr_result,
        "power": power,
        "signal": signal,
        "thermal": thermal,
        "layout": layout,
        "gnn": gnn,
        "final": final_report
    }


# ----------------------------------------
# ⚡ STREAMLIT CACHE
# ----------------------------------------
@st.cache_data(show_spinner=True)
def cached_full_analysis(image_path, graph_summary, gnn_output, ocr_text):
    return run_full_analysis(image_path, graph_summary, gnn_output, ocr_text)


# ----------------------------------------
# 🎯 LIGHT MODE (FAST)
# ----------------------------------------
def quick_analysis(image_path, graph_summary):

    vision = run_vision_agent(image_path, use_llm_refinement=False)

    context = f"""
    Vision: {vision}
    Graph: {graph_summary}
    """

    return {
        "vision": vision,
        "quick_insight": context
    }
