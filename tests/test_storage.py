import json
import tempfile
import unittest
from pathlib import Path
from campusflow.storage import StorageError, load_tickets, save_tickets
from campusflow.tickets import create_ticket

class StorageTests(unittest.TestCase):
    def test_missing_file_starts_empty(self):
        with tempfile.TemporaryDirectory() as d: self.assertEqual(load_tickets(Path(d) / "missing.json"), [])
    def test_save_reload_and_next_id(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "data" / "tickets.json"
            tickets = []
            create_ticket(tickets, "Wi-Fi", "Network", "high", 12)
            save_tickets(path, tickets)
            loaded = load_tickets(path)
            self.assertEqual(loaded, tickets)
            self.assertEqual(create_ticket(loaded, "Laptop", "Hardware", "low", 1)["id"], "T002")
    def test_malformed_json_is_not_erased(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "tickets.json"
            path.write_text("{broken", encoding="utf-8")
            with self.assertRaises(StorageError): load_tickets(path)
            self.assertEqual(path.read_text(encoding="utf-8"), "{broken")
    def test_duplicate_ids_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "tickets.json"
            t = {"id":"T001","title":"x","category":"Other","urgency":"low","affected_users":1,
                 "priority":"low","status":"open","assigned_to":None}
            path.write_text(json.dumps([t, t]), encoding="utf-8")
            with self.assertRaises(StorageError): load_tickets(path)

if __name__ == "__main__": unittest.main()
