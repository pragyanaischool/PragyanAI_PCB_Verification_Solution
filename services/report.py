"""
Report Service

Combines:
- Rule Engine output
- Multi-agent AI outputs

Generates:
- Unified issue list
- Score
- Summary
- Category-wise breakdown
"""

from typing import Dict, List


# ----------------------------------------
# 🧠 NORMALIZE ISSUES
# ----------------------------------------
def normalize_issues(agent_name: str, result) -> List[Dict]:

    issues = []

    if isinstance(result, dict) and "issues" in result:
        for issue in result["issues"]:
            issues.append({
                "category": agent_name,
                "issue": issue.get("issue", ""),
                "severity": issue.get("severity", "Medium"),
                "explanation": issue.get("explanation", ""),
                "fix": issue.get("fix", "")
            })

    return issues


# ----------------------------------------
# 🔗 MERGE ALL ISSUES
# ----------------------------------------
def merge_all_issues(rule_issues: List[Dict], agent_outputs: Dict):

    all_issues = []

    # Add rule issues
    for r in rule_issues:
        all_issues.append({
            "category": r.get("category", "Rule"),
            "issue": r.get("issue", ""),
            "severity": r.get("severity", "Medium"),
            "explanation": r.get("explanation", ""),
            "fix": r.get("fix", "")
        })

    # Add agent issues
    for agent_name, output in agent_outputs.items():
        all_issues.extend(normalize_issues(agent_name, output))

    return all_issues


# ----------------------------------------
# 📊 SEVERITY COUNT
# ----------------------------------------
def severity_breakdown(issues: List[Dict]):

    stats = {"high": 0, "medium": 0, "low": 0}

    for i in issues:
        s = i.get("severity", "").lower()

        if s == "high":
            stats["high"] += 1
        elif s == "medium":
            stats["medium"] += 1
        elif s == "low":
            stats["low"] += 1

    return stats


# ----------------------------------------
# 🎯 SCORE CALCULATION
# ----------------------------------------
def calculate_score(issues: List[Dict]):

    score = 100

    for i in issues:
        s = i.get("severity", "").lower()

        if s == "high":
            score -= 10
        elif s == "medium":
            score -= 5
        elif s == "low":
            score -= 2

    return max(score, 0)


# ----------------------------------------
# 🧾 EXECUTIVE SUMMARY
# ----------------------------------------
def generate_summary(issues: List[Dict], stats: Dict):

    total = len(issues)

    if total == 0:
        return "PCB design looks clean with no major issues."

    summary = f"""
    PCB Analysis Summary:

    - Total Issues: {total}
    - High Severity: {stats['high']}
    - Medium Severity: {stats['medium']}
    - Low Severity: {stats['low']}

    """

    if stats["high"] > 0:
        summary += "⚠️ Critical issues detected. Immediate attention required.\n"
    elif stats["medium"] > 0:
        summary += "⚡ Moderate issues present. Optimization recommended.\n"
    else:
        summary += "✅ Minor issues only. Design is stable.\n"

    return summary.strip()


# ----------------------------------------
# 🧠 FINAL REPORT GENERATOR
# ----------------------------------------
def generate_report(rule_issues: List[Dict], agent_outputs: Dict):

    # Step 1: Merge
    all_issues = merge_all_issues(rule_issues, agent_outputs)

    # Step 2: Stats
    stats = severity_breakdown(all_issues)

    # Step 3: Score
    score = calculate_score(all_issues)

    # Step 4: Summary
    summary = generate_summary(all_issues, stats)

    return {
        "score": score,
        "summary": summary,
        "issue_count": len(all_issues),
        "severity": stats,
        "issues": all_issues
    }


# ----------------------------------------
# 📊 CATEGORY-WISE REPORT
# ----------------------------------------
def category_breakdown(issues: List[Dict]):

    categories = {}

    for issue in issues:
        cat = issue.get("category", "Other")

        if cat not in categories:
            categories[cat] = []

        categories[cat].append(issue)

    return categories


# ----------------------------------------
# 📈 PRIORITIZED ISSUES
# ----------------------------------------
def prioritize_issues(issues: List[Dict]):

    priority_map = {"high": 0, "medium": 1, "low": 2}

    return sorted(
        issues,
        key=lambda x: priority_map.get(x.get("severity", "medium").lower(), 1)
    )


# ----------------------------------------
# 📦 FULL ENTERPRISE REPORT
# ----------------------------------------
def build_enterprise_report(rule_issues: List[Dict], agent_outputs: Dict):

    base = generate_report(rule_issues, agent_outputs)

    prioritized = prioritize_issues(base["issues"])
    category_view = category_breakdown(base["issues"])

    return {
        **base,
        "prioritized_issues": prioritized[:10],  # top issues
        "categories": category_view
    }
  
