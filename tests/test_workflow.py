import unittest
from campusflow.queue import work_queue
from campusflow.reports import build_report
from campusflow.tickets import TicketValidationError, create_ticket
from campusflow.workflow import assign_ticket, change_status, reopen_ticket

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tickets = []
        create_ticket(self.tickets, "Low", "Other", "low", 1)
        create_ticket(self.tickets, "Critical", "Network", "high", 12)
        create_ticket(self.tickets, "High", "Hardware", "high", 2)
    def test_unknown_ticket_rejected(self):
        with self.assertRaises(TicketValidationError): assign_ticket(self.tickets, "T999", "Ada")
    def test_blank_staff_rejected(self):
        with self.assertRaises(TicketValidationError): assign_ticket(self.tickets, "T001", " ")
    def test_unassigned_ticket_cannot_start(self):
        with self.assertRaises(TicketValidationError): change_status(self.tickets, "T001", "in_progress")
    def test_assigned_ticket_progresses_to_resolved(self):
        assign_ticket(self.tickets, "T001", "Ada")
        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")
        self.assertEqual(self.tickets[0]["status"], "resolved")
    def test_invalid_transition_rejected(self):
        with self.assertRaises(TicketValidationError): change_status(self.tickets, "T001", "resolved")
    def test_resolved_ticket_requires_reopen_before_modification(self):
        assign_ticket(self.tickets, "T001", "Ada")
        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")
        with self.assertRaises(TicketValidationError): assign_ticket(self.tickets, "T001", "Grace")
        reopen_ticket(self.tickets, "T001")
        assign_ticket(self.tickets, "T001", "Grace")
        self.assertEqual(self.tickets[0]["assigned_to"], "Grace")
        self.assertEqual(self.tickets[0]["status"], "open")
    def test_queue_priority_then_numeric_id(self):
        create_ticket(self.tickets, "Critical later", "Network", "high", 10)
        self.assertEqual([t["id"] for t in work_queue(self.tickets)], ["T002", "T004", "T003", "T001"])
    def test_queue_excludes_non_open(self):
        assign_ticket(self.tickets, "T002", "Ada")
        change_status(self.tickets, "T002", "in_progress")
        self.assertNotIn("T002", [t["id"] for t in work_queue(self.tickets)])
    def test_reports_and_empty_report(self):
        report = build_report(self.tickets)
        self.assertEqual(report["total"], 3)
        self.assertEqual(report["by_priority"]["critical"], 1)
        self.assertEqual(build_report([])["by_status"]["resolved"], 0)

if __name__ == "__main__": unittest.main()
