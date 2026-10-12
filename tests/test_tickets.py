import unittest
from campusflow.tickets import TicketValidationError, calculate_priority, create_ticket, find_ticket

class PriorityTests(unittest.TestCase):
    def test_high_12_is_critical(self): self.assertEqual(calculate_priority("high", 12), "critical")
    def test_high_2_is_high(self): self.assertEqual(calculate_priority("high", 2), "high")
    def test_low_4_is_medium(self): self.assertEqual(calculate_priority("low", 4), "medium")
    def test_low_1_is_low(self): self.assertEqual(calculate_priority("low", 1), "low")
    def test_ten_users_is_high_even_if_low_urgency(self): self.assertEqual(calculate_priority("low", 10), "high")
    def test_medium_urgency_is_medium(self): self.assertEqual(calculate_priority("medium", 1), "medium")

class TicketCreationTests(unittest.TestCase):
    def setUp(self): self.tickets = []
    def test_creation_normalizes_values_and_generates_id(self):
        t = create_ticket(self.tickets, " Wi-Fi ", "network", "HIGH", "12")
        self.assertEqual((t["id"], t["title"], t["category"], t["urgency"], t["affected_users"]),
                         ("T001", "Wi-Fi", "Network", "high", 12))
    def test_blank_title_rejected_without_mutation(self):
        with self.assertRaises(TicketValidationError): create_ticket(self.tickets, " ", "Network", "low", 1)
        self.assertEqual(self.tickets, [])
    def test_zero_users_rejected(self):
        with self.assertRaises(TicketValidationError): create_ticket(self.tickets, "Issue", "Other", "low", 0)
        self.assertEqual(self.tickets, [])
    def test_decimal_users_rejected(self):
        with self.assertRaises(TicketValidationError): create_ticket(self.tickets, "Issue", "Other", "low", "2.5")
    def test_invalid_category_and_urgency_rejected(self):
        with self.assertRaises(TicketValidationError): create_ticket(self.tickets, "Issue", "Food", "low", 1)
        with self.assertRaises(TicketValidationError): create_ticket(self.tickets, "Issue", "Other", "urgent", 1)
    def test_id_uses_highest_existing_number(self):
        create_ticket(self.tickets, "First", "Other", "low", 1)
        self.tickets.append({"id": "T009"})
        self.assertEqual(create_ticket(self.tickets, "Next", "Other", "low", 1)["id"], "T010")
    def test_find_ticket_ignores_id_case(self):
        create_ticket(self.tickets, "First", "Other", "low", 1)
        self.assertEqual(find_ticket(self.tickets, "t001")["title"], "First")

if __name__ == "__main__": unittest.main()
