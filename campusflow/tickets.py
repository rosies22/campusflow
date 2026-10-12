from typing import Any

CATEGORIES = ("Network", "Hardware", "Software", "Other")
URGENCY_LEVELS = ("low", "medium", "high")
PRIORITIES = ("critical", "high", "medium", "low")

class TicketValidationError(ValueError):
    """Raised when ticket input is invalid."""

def calculate_priority(urgency: str, affected_users: int) -> str:
    """Apply priority rules in the required order."""
    urgency = str(urgency).strip().lower()
    if urgency not in URGENCY_LEVELS:
        raise TicketValidationError(f"Urgency must be one of: {', '.join(URGENCY_LEVELS)}.")
    if isinstance(affected_users, bool) or not isinstance(affected_users, int) or affected_users <= 0:
        raise TicketValidationError("Affected users must be a positive integer.")
    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"

def _positive_integer(value: Any) -> int:
    if isinstance(value, bool):
        raise TicketValidationError("Affected users must be a positive integer.")
    if isinstance(value, int):
        number = value
    elif isinstance(value, str) and value.strip().isdigit():
        number = int(value.strip())
    else:
        raise TicketValidationError("Affected users must be a whole number (for example, 3).")
    if number <= 0:
        raise TicketValidationError("Affected users must be greater than zero.")
    return number

def create_ticket(tickets: list[dict[str, Any]], title: str, category: str,
                  urgency: str, affected_users: Any) -> dict[str, Any]:
    clean_title = str(title).strip()
    if not clean_title:
        raise TicketValidationError("Title must not be blank.")
    categories = {item.lower(): item for item in CATEGORIES}
    clean_category = categories.get(str(category).strip().lower())
    if clean_category is None:
        raise TicketValidationError(f"Category must be one of: {', '.join(CATEGORIES)}.")
    clean_urgency = str(urgency).strip().lower()
    if clean_urgency not in URGENCY_LEVELS:
        raise TicketValidationError(f"Urgency must be one of: {', '.join(URGENCY_LEVELS)}.")
    count = _positive_integer(affected_users)
    priority = calculate_priority(clean_urgency, count)
    highest = 0
    for ticket in tickets:
        tid = str(ticket.get("id", ""))
        if tid.startswith("T") and tid[1:].isdigit():
            highest = max(highest, int(tid[1:]))
    ticket = {"id": f"T{highest + 1:03d}", "title": clean_title,
              "category": clean_category, "urgency": clean_urgency,
              "affected_users": count, "priority": priority,
              "status": "open", "assigned_to": None}
    tickets.append(ticket)
    return ticket

def find_ticket(tickets: list[dict[str, Any]], ticket_id: str) -> dict[str, Any]:
    wanted = str(ticket_id).strip().upper()
    for ticket in tickets:
        if str(ticket.get("id", "")).upper() == wanted:
            return ticket
    raise TicketValidationError(f"Ticket '{wanted}' was not found.")
