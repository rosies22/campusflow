from collections import Counter
STATUSES = ("open", "in_progress", "resolved")
PRIORITIES = ("critical", "high", "medium", "low")

def build_report(tickets):
    statuses = Counter(t.get("status", "unknown") for t in tickets)
    priorities = Counter(t.get("priority", "unknown") for t in tickets)
    return {"total": len(tickets),
            "by_status": {s: statuses.get(s, 0) for s in STATUSES},
            "by_priority": {p: priorities.get(p, 0) for p in PRIORITIES}}
