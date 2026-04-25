"""
Graph Service

Builds PCB graph representation from parsed data.

Supports:
- Node creation (components)
- Edge creation (nets)
- Feature extraction for GNN
- Graph summary utilities
"""

import networkx as nx
import math
from typing import Dict, List, Tuple


# ----------------------------------------
# 🧠 MAIN GRAPH BUILDER
# ----------------------------------------
def build_graph(pcb_data: Dict) -> nx.Graph:

    G = nx.Graph()

    components = pcb_data.get("components", [])
    nets = pcb_data.get("nets", [])

    # Add nodes
    for comp in components:
        G.add_node(comp, type=detect_component_type(comp))

    # Add edges
    for n1, n2 in nets:
        if n1 in G.nodes and n2 in G.nodes:
            G.add_edge(n1, n2)

    return G


# ----------------------------------------
# 🔍 COMPONENT TYPE DETECTION
# ----------------------------------------
def detect_component_type(name: str) -> str:

    if name.startswith("R"):
        return "Resistor"
    elif name.startswith("C"):
        return "Capacitor"
    elif name.startswith("U"):
        return "IC"
    elif name.startswith("L"):
        return "Inductor"
    elif name.startswith("D"):
        return "Diode"
    elif name.startswith("Q"):
        return "Transistor"
    return "Unknown"


# ----------------------------------------
# 📊 GRAPH SUMMARY
# ----------------------------------------
def graph_summary(graph: nx.Graph) -> str:

    return f"Nodes={graph.number_of_nodes()}, Edges={graph.number_of_edges()}"


# ----------------------------------------
# 🔗 DEGREE ANALYSIS
# ----------------------------------------
def node_degrees(graph: nx.Graph) -> Dict:

    return dict(graph.degree())


# ----------------------------------------
# ⚠️ FIND DISCONNECTED NODES
# ----------------------------------------
def find_isolated_nodes(graph: nx.Graph) -> List[str]:

    return list(nx.isolates(graph))


# ----------------------------------------
# 🔥 FIND HIGH DEGREE NODES
# ----------------------------------------
def find_high_degree_nodes(graph: nx.Graph, threshold: int = 5):

    return [node for node, deg in graph.degree() if deg > threshold]


# ----------------------------------------
# 🔄 GRAPH TO EDGE LIST
# ----------------------------------------
def graph_to_edges(graph: nx.Graph) -> List[Tuple[str, str]]:

    return list(graph.edges())


# ----------------------------------------
# 🧠 GRAPH FEATURES (FOR GNN)
# ----------------------------------------
def graph_features(graph: nx.Graph):

    features = []

    for node in graph.nodes(data=True):
        name = node[0]
        node_type = node[1].get("type", "Unknown")

        features.append([
            len(name),                  # simple feature
            hash(node_type) % 1000      # encoded type
        ])

    return features


# ----------------------------------------
# 📐 DISTANCE BASED GRAPH (IMAGE MODE)
# ----------------------------------------
def build_spatial_graph(components: List[Dict], distance_threshold=150):

    """
    Build graph using spatial proximity (from vision model)
    """

    G = nx.Graph()

    # Add nodes
    for i, comp in enumerate(components):
        G.add_node(i, pos=comp["center"], type=comp.get("type", "Unknown"))

    # Connect based on distance
    for i in range(len(components)):
        for j in range(i + 1, len(components)):

            x1, y1 = components[i]["center"]
            x2, y2 = components[j]["center"]

            dist = math.hypot(x1 - x2, y1 - y2)

            if dist < distance_threshold:
                G.add_edge(i, j, weight=dist)

    return G


# ----------------------------------------
# 🔄 MERGE MULTIPLE GRAPHS
# ----------------------------------------
def merge_graphs(graph_list: List[nx.Graph]) -> nx.Graph:

    merged = nx.Graph()

    for g in graph_list:
        merged = nx.compose(merged, g)

    return merged


# ----------------------------------------
# 📊 CONNECTIVITY CHECK
# ----------------------------------------
def is_connected(graph: nx.Graph) -> bool:

    if graph.number_of_nodes() == 0:
        return False

    return nx.is_connected(graph)


# ----------------------------------------
# 🔍 COMPONENT CLUSTERS
# ----------------------------------------
def find_clusters(graph: nx.Graph):

    return list(nx.connected_components(graph))


# ----------------------------------------
# ⚡ CRITICAL NODES (CUT VERTICES)
# ----------------------------------------
def critical_nodes(graph: nx.Graph):

    return list(nx.articulation_points(graph))


# ----------------------------------------
# 🔁 GRAPH TO DICT (SERIALIZATION)
# ----------------------------------------
def graph_to_dict(graph: nx.Graph):

    return {
        "nodes": list(graph.nodes(data=True)),
        "edges": list(graph.edges())
    }
