"""
Rule Engine Service (DRC-like checks)

Provides:
- Basic electrical sanity checks
- Connectivity validation
- Heuristic PCB design rules
- Severity tagging
"""

from typing import List, Dict
import networkx as nx


# ----------------------------------------
# 🚀 MAIN RULE ENGINE
# ----------------------------------------
def run_rules(graph: nx.Graph) -> List[Dict]:

    issues = []

    issues += check_floating_components(graph)
    issues += check_high_degree_nodes(graph)
    issues += check_isolated_clusters(graph)
    issues += check_critical_nodes(graph)
    issues += check_sparse_connectivity(graph)

    return issues


# ----------------------------------------
# ⚠️ FLOATING COMPONENTS
# ----------------------------------------
def check_floating_components(graph: nx.Graph):

    issues = []

    for node in graph.nodes:
        if graph.degree[node] == 0:
            issues.append({
                "category": "Connectivity",
                "issue": "Floating Component",
                "node": node,
                "severity": "High",
                "explanation": "Component is not connected to any net",
                "fix": "Ensure proper net connection"
            })

    return issues


# ----------------------------------------
# 🔥 HIGH DEGREE NODES (POSSIBLE SHORT / OVERLOAD)
# ----------------------------------------
def check_high_degree_nodes(graph: nx.Graph, threshold: int = 6):

    issues = []

    for node, degree in graph.degree():
        if degree > threshold:
            issues.append({
                "category": "Connectivity",
                "issue": "Overconnected Node",
                "node": node,
                "severity": "Medium",
                "explanation": f"Node has {degree} connections (threshold {threshold})",
                "fix": "Verify if connections are correct or unintended shorts"
            })

    return issues


# ----------------------------------------
# 🔗 ISOLATED CLUSTERS
# ----------------------------------------
def check_isolated_clusters(graph: nx.Graph):

    issues = []

    clusters = list(nx.connected_components(graph))

    if len(clusters) > 1:
        issues.append({
            "category": "Connectivity",
            "issue": "Disconnected Clusters",
            "severity": "High",
            "explanation": f"PCB has {len(clusters)} disconnected sub-networks",
            "fix": "Ensure all required nets are properly connected"
        })

    return issues


# ----------------------------------------
# ⚡ CRITICAL NODES (CUT VERTICES)
# ----------------------------------------
def check_critical_nodes(graph: nx.Graph):

    issues = []

    try:
        critical = list(nx.articulation_points(graph))

        for node in critical:
            issues.append({
                "category": "Reliability",
                "issue": "Critical Node",
                "node": node,
                "severity": "Medium",
                "explanation": "Failure of this node disconnects circuit",
                "fix": "Add redundancy or alternate routing"
            })

    except:
        pass

    return issues


# ----------------------------------------
# 📉 SPARSE CONNECTIVITY
# ----------------------------------------
def check_sparse_connectivity(graph: nx.Graph):

    issues = []

    if graph.number_of_nodes() == 0:
        return issues

    avg_degree = sum(dict(graph.degree()).values()) / graph.number_of_nodes()

    if avg_degree < 1.5:
        issues.append({
            "category": "Design",
            "issue": "Sparse Connectivity",
            "severity": "Medium",
            "explanation": f"Average degree is low ({avg_degree:.2f})",
            "fix": "Verify missing connections or incomplete routing"
        })

    return issues


# ----------------------------------------
# 🧠 RULE SUMMARY
# ----------------------------------------
def summarize_rules(issues: List[Dict]):

    summary = {
        "total_issues": len(issues),
        "high": 0,
        "medium": 0,
        "low": 0
    }

    for issue in issues:
        severity = issue.get("severity", "").lower()

        if severity == "high":
            summary["high"] += 1
        elif severity == "medium":
            summary["medium"] += 1
        elif severity == "low":
            summary["low"] += 1

    return summary


# ----------------------------------------
# 📊 RULE SCORE
# ----------------------------------------
def rule_score(issues: List[Dict]):

    score = 100

    for issue in issues:
        severity = issue.get("severity", "").lower()

        if severity == "high":
            score -= 10
        elif severity == "medium":
            score -= 5
        elif severity == "low":
            score -= 2

    return max(score, 0)
