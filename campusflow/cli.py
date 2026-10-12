from .queue import work_queue
from .reports import build_report
from .storage import StorageError
from .tickets import CATEGORIES, URGENCY_LEVELS, TicketValidationError, create_ticket, find_ticket
from .workflow import STATUSES, assign_ticket, change_status, reopen_ticket

def show_ticket(ticket):
    for field in ("id", "title", "category", "urgency", "affected_users", "priority", "status", "assigned_to"):
        print(f"  {field}: {ticket.get(field)}")

def run_cli(tickets, save_callback):
    menu = """
=== CampusFlow Helpdesk ===
1. Create ticket
2. List all tickets
3. View one ticket
4. Assign ticket
5. Change ticket status
6. Reopen resolved ticket
7. Show work queue
8. Show reports
9. Exit
"""
    while True:
        print(menu)
        choice = input("Choose an option (1-9): ").strip()
        try:
            if choice == "1":
                ticket = create_ticket(tickets, input("Title: "), input(f"Category {CATEGORIES}: "),
                                       input(f"Urgency {URGENCY_LEVELS}: "), input("Affected users: "))
                save_callback(tickets)
                print("Ticket created:")
                show_ticket(ticket)
            elif choice == "2":
                if not tickets:
                    print("No tickets yet.")
                for ticket in tickets:
                    show_ticket(ticket)
            elif choice == "3":
                show_ticket(find_ticket(tickets, input("Ticket ID: ")))
            elif choice == "4":
                ticket = assign_ticket(tickets, input("Ticket ID: "), input("Staff member name: "))
                save_callback(tickets)
                print("Ticket assigned.")
                show_ticket(ticket)
            elif choice == "5":
                ticket = change_status(tickets, input("Ticket ID: "), input(f"New status {STATUSES}: "))
                save_callback(tickets)
                print("Status updated.")
                show_ticket(ticket)
            elif choice == "6":
                ticket = reopen_ticket(tickets, input("Ticket ID: "))
                save_callback(tickets)
                print("Ticket reopened.")
                show_ticket(ticket)
            elif choice == "7":
                queue = work_queue(tickets)
                if not queue:
                    print("The open work queue is empty.")
                for t in queue:
                    print(f"{t['id']} | {t['priority']} | {t['title']} | assigned: {t['assigned_to']}")
            elif choice == "8":
                report = build_report(tickets)
                print(f"Total tickets: {report['total']}")
                for group in ("by_status", "by_priority"):
                    print(group.replace("_", " ").title() + ":")
                    for key, value in report[group].items():
                        print(f"  {key}: {value}")
            elif choice == "9":
                save_callback(tickets)
                print("Goodbye.")
                return
            else:
                print("Choose a number from 1 to 9.")
        except (TicketValidationError, StorageError, OSError) as exc:
            print(f"Error: {exc}")
