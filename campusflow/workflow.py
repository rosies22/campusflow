from .tickets import TicketValidationError, find_ticket
STATUSES = ("open", "in_progress", "resolved")

def assign_ticket(tickets, ticket_id, staff_name):
    ticket = find_ticket(tickets, ticket_id)
    if ticket["status"] == "resolved":
        raise TicketValidationError("Reopen a resolved ticket before modifying it.")
    name = str(staff_name).strip()
    if not name:
        raise TicketValidationError("Staff member name must not be blank.")
    ticket["assigned_to"] = name
    return ticket

def change_status(tickets, ticket_id, new_status):
    ticket = find_ticket(tickets, ticket_id)
    target = str(new_status).strip().lower()
    if target not in STATUSES:
        raise TicketValidationError(f"Status must be one of: {', '.join(STATUSES)}.")
    current = ticket["status"]
    if current == "resolved":
        raise TicketValidationError("Resolved tickets must be reopened before further changes.")
    if current == "open" and target == "in_progress":
        if not ticket.get("assigned_to"):
            raise TicketValidationError("Assign the ticket before moving it to in_progress.")
        ticket["status"] = target
        return ticket
    if current == "in_progress" and target == "resolved":
        ticket["status"] = target
        return ticket
    if target == current:
        raise TicketValidationError(f"Ticket is already {current}.")
    raise TicketValidationError(f"Invalid transition: {current} -> {target}. Use open -> in_progress -> resolved.")

def reopen_ticket(tickets, ticket_id):
    ticket = find_ticket(tickets, ticket_id)
    if ticket["status"] != "resolved":
        raise TicketValidationError("Only a resolved ticket can be reopened.")
    ticket["status"] = "open"
    return ticket
