import json
import os
from pathlib import Path

class StorageError(RuntimeError):
    """Raised when ticket data cannot safely be loaded or saved."""

def load_tickets(path):
    path = Path(path)
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise StorageError(f"Malformed JSON in '{path}': {exc}") from exc
    except OSError as exc:
        raise StorageError(f"Could not read '{path}': {exc}") from exc
    if not isinstance(data, list) or any(not isinstance(item, dict) for item in data):
        raise StorageError(f"'{path}' must contain a JSON list of ticket objects.")
    required = {"id", "title", "category", "urgency", "affected_users", "priority", "status", "assigned_to"}
    ids = []
    for index, ticket in enumerate(data):
        missing = required - ticket.keys()
        if missing:
            raise StorageError(f"Ticket at index {index} is missing fields: {', '.join(sorted(missing))}.")
        ids.append(str(ticket["id"]))
    if len(ids) != len(set(ids)):
        raise StorageError(f"'{path}' contains duplicate ticket IDs.")
    return data

def save_tickets(path, tickets):
    path = Path(path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temp = path.with_suffix(path.suffix + ".tmp")
        with temp.open("w", encoding="utf-8") as handle:
            json.dump(tickets, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        os.replace(temp, path)
    except OSError as exc:
        raise StorageError(f"Could not save '{path}': {exc}") from exc
