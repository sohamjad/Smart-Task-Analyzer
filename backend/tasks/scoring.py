# scoring.py
from dateutil import parser
from datetime import datetime, timedelta

DEFAULT_WEIGHTS = {
    "urgency": 0.4,
    "importance": 0.4,
    "effort": 0.1,
    "dependency": 0.1
}

# -------------------------
# CIRCULAR DEPENDENCY CHECK
# -------------------------
def detect_cycles(tasks):
    graph = {t["id"]: t.get("dependencies", []) for t in tasks}
    visited = set()
    stack = set()
    cycles = set()

    def dfs(node):
        if node in stack:
            cycles.add(node)
            return True
        if node in visited:
            return False

        visited.add(node)
        stack.add(node)

        for dep in graph.get(node, []):
            if dep in graph:  # Only check known tasks
                if dfs(dep):
                    cycles.add(node)
                    return True

        stack.remove(node)
        return False

    for node in graph:
        dfs(node)

    return cycles


# -------------------------
# SCORING FUNCTION
# -------------------------
def score_tasks(tasks, weights=DEFAULT_WEIGHTS):
    today = datetime.now().date()

    # First: detect cycles
    cycles = detect_cycles(tasks)

    scored = []
    for t in tasks:
        explanation = []

        # If circular dependency:
        if t["id"] in cycles:
            scored.append({
                **t,
                "score": 0,
                "explanation": "Circular dependency detected. Resolve this first."
            })
            continue

        # --- urgency ---
        if t.get("due_date"):
            due = parser.parse(t["due_date"]).date()
            days_left = (due - today).days

            if days_left < 0:
                urgency_score = 100
                explanation.append("Past due date → very urgent")
            elif days_left == 0:
                urgency_score = 90
                explanation.append("Due today → urgent")
            else:
                urgency_score = max(10, 100 - days_left * 5)
                explanation.append(f"Due in {days_left} days")

        else:
            urgency_score = 30
            explanation.append("No due date")

        # --- importance ---
        importance_score = t.get("importance", 5) * 10
        explanation.append(f"Importance = {t.get('importance',5)}")

        # --- effort ---
        effort_score = max(5, 30 - (t.get("estimated_hours", 1) * 3))
        explanation.append(f"Effort: {t.get('estimated_hours', 1)} hrs")

        # --- dependency weight ---
        dep_count = len(t.get("dependencies", []))
        dependency_score = min(dep_count * 10, 40)
        explanation.append(f"{dep_count} dependencies")

        # Final score
        final_score = (
            urgency_score * weights["urgency"] +
            importance_score * weights["importance"] +
            effort_score * weights["effort"] +
            dependency_score * weights["dependency"]
        )

        scored.append({
            **t,
            "score": round(final_score, 2),
            "explanation": "; ".join(explanation)
        })

    return scored
