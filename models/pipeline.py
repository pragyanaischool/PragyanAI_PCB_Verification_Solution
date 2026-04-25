from models.vision.yolo_detector import detect_components
from models.vision.ocr_model import extract_text
from models.vision.segmentation_model import segment_pcb, overlay_mask
from models.graph.graph_builder import build_graph
from models.gnn.gnn_model import PCB_GNN
from ai.agents import explain_results

def run_full_pipeline(image_path):

    components = detect_components(image_path)
    ocr = extract_text(image_path)

    mask = segment_pcb(image_path)
    overlay = overlay_mask(image_path, mask)

    graph = build_graph(components)

    graph_summary = f"Nodes: {len(graph.nodes)}, Edges: {len(graph.edges)}"

    gnn_output = "Potential routing issue detected"

    explanation = explain_results(graph_summary, gnn_output, ocr)

    return {
        "components": components,
        "ocr": ocr,
        "graph": graph_summary,
        "analysis": explanation,
        "overlay": overlay
    }
