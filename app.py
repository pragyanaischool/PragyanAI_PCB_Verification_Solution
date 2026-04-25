import streamlit as st
from PIL import Image
import tempfile
import traceback

# Services
from services.parser import parse_pcb
from services.graph import build_graph, graph_summary
from services.rules import run_rules

# AI Orchestrator
from ai.orchestrator import run_full_analysis

# Utils
from utils.file import save_uploaded_file, safe_delete
from utils.cache import st_cache_data_wrapper

# ----------------------------------------
# 🎨 PAGE CONFIG
# ----------------------------------------
st.set_page_config(
    page_title="PragyanAI PCB Copilot",
    layout="wide",
    page_icon="⚡"
)

# ----------------------------------------
# 🧠 HEADER
# ----------------------------------------
st.title("⚡ PragyanAI PCB Copilot")
st.caption("Multi-Agent AI for PCB Analysis (Vision + Graph + LLM + GNN)")

# ----------------------------------------
# 📤 SIDEBAR SETTINGS
# ----------------------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    run_mode = st.selectbox(
        "Analysis Mode",
        ["Full (Accurate)", "Quick (Fast)"]
    )

    show_raw = st.checkbox("Show Raw Outputs", value=False)
    cleanup_files_flag = st.checkbox("Cleanup temp files", value=True)

    st.markdown("---")
    st.markdown("### ℹ️ Info")
    st.markdown("""
    - Multi-Agent AI  
    - Power / Signal / Thermal / Layout  
    - Vision + OCR + Graph + GNN  
    """)

# ----------------------------------------
# 📤 FILE UPLOAD
# ----------------------------------------
col1, col2 = st.columns([2, 1])

with col1:
    pcb_file = st.file_uploader(
        "Upload PCB Image or Netlist",
        type=["png", "jpg", "jpeg", "txt", "net", "netlist"]
    )

with col2:
    st.markdown("### 🧩 Supported Inputs")
    st.markdown("""
    - PCB Images  
    - Netlist Files  
    """)

# ----------------------------------------
# 🖼️ PREVIEW
# ----------------------------------------
if pcb_file:

    file_type = pcb_file.type

    if "image" in file_type:
        image = Image.open(pcb_file)
        st.image(image, caption="PCB Preview", use_container_width=True)

# ----------------------------------------
# 🚀 ANALYSIS BUTTON
# ----------------------------------------
if pcb_file:

    if st.button("🚀 Run AI Analysis"):

        try:
            with st.spinner("Running full AI pipeline..."):

                # ----------------------------------------
                # 💾 SAVE FILE
                # ----------------------------------------
                file_path = save_uploaded_file(pcb_file)

                # ----------------------------------------
                # 🧠 PARSER
                # ----------------------------------------
                pcb_data = parse_pcb(file_path)

                # ----------------------------------------
                # 🔗 GRAPH
                # ----------------------------------------
                graph = build_graph(pcb_data)
                g_summary = graph_summary(graph)

                # ----------------------------------------
                # ⚠️ RULE ENGINE
                # ----------------------------------------
                rule_issues = run_rules(graph)

                # ----------------------------------------
                # 🧠 MOCK (Replace with real later)
                # ----------------------------------------
                gnn_output = "Graph anomaly detected near power node"
                ocr_text = pcb_data.get("raw_text", "U1 R1 C1 5V GND")

                # ----------------------------------------
                # 🤖 AI ORCHESTRATOR
                # ----------------------------------------
                result = run_full_analysis(
                    image_path=file_path,
                    graph_summary=g_summary,
                    gnn_output=gnn_output,
                    ocr_text=ocr_text
                )

            st.success("✅ Analysis Completed")

            # ----------------------------------------
            # 📊 DISPLAY RESULTS
            # ----------------------------------------
            tab1, tab2, tab3, tab4 = st.tabs([
                "🧠 Final Report",
                "⚡ Domain Insights",
                "📊 Graph & Rules",
                "🔍 Raw Data"
            ])

            # ----------------------------------------
            # 🧠 FINAL REPORT
            # ----------------------------------------
            with tab1:
                final = result.get("final", {})

                st.metric("PCB Score", final.get("score", 0))

                st.subheader("📋 Summary")
                st.write(final.get("summary", ""))

                st.subheader("⚠️ Issues")
                st.json(final.get("issues", []))

            # ----------------------------------------
            # ⚡ DOMAIN AGENTS
            # ----------------------------------------
            with tab2:

                cols = st.columns(2)

                with cols[0]:
                    st.subheader("⚡ Power")
                    st.write(result.get("power"))

                    st.subheader("🔌 Signal")
                    st.write(result.get("signal"))

                with cols[1]:
                    st.subheader("🌡️ Thermal")
                    st.write(result.get("thermal"))

                    st.subheader("🧩 Layout")
                    st.write(result.get("layout"))

            # ----------------------------------------
            # 📊 GRAPH + RULES
            # ----------------------------------------
            with tab3:

                st.subheader("Graph Summary")
                st.write(g_summary)

                st.subheader("Rule Issues")
                st.json(rule_issues)

            # ----------------------------------------
            # 🔍 RAW OUTPUTS
            # ----------------------------------------
            if show_raw:
                with tab4:
                    st.json(result)

            # ----------------------------------------
            # 🧹 CLEANUP
            # ----------------------------------------
            if cleanup_files_flag:
                safe_delete(file_path)

        except Exception as e:
            st.error("❌ Error during processing")
            st.text(str(e))
            st.text(traceback.format_exc())

# ----------------------------------------
# 🧭 FOOTER
# ----------------------------------------
st.markdown("---")
st.markdown("⚡ PragyanAI | PCB Copilot | Multi-Agent AI System")
