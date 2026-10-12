from pathlib import Path
from campusflow.cli import run_cli
from campusflow.storage import StorageError, load_tickets, save_tickets

DATA_PATH = Path(__file__).resolve().parent / "data" / "tickets.json"

def main():
    try:
        tickets = load_tickets(DATA_PATH)
    except StorageError as exc:
        print(f"Cannot load ticket data: {exc}")
        print("The data file was not overwritten. Fix or restore it before restarting.")
        return
    try:
        run_cli(tickets, save_callback=lambda current: save_tickets(DATA_PATH, current))
    except (OSError, StorageError) as exc:
        print(f"Could not save ticket data: {exc}")

if __name__ == "__main__":
    main()
