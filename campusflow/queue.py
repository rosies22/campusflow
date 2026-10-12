from .tickets import PRIORITIES
_PRIORITY_RANK = {priority: i for i, priority in enumerate(PRIORITIES)}

def work_queue(tickets):
    """Return open tickets by priority, then numeric ticket ID."""
    open_tickets = [t for t in tickets if t.get("status") == "open"]
    def key(ticket):
        tid = str(ticket.get("id", ""))
        number = int(tid[1:]) if tid.startswith("T") and tid[1:].isdigit() else 10**12
        return _PRIORITY_RANK.get(ticket.get("priority"), len(_PRIORITY_RANK)), number
    return sorted(open_tickets, key=key)
