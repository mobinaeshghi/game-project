import unittest
from decimal import Decimal

from delivery_system import DeliverySystem


class TestDriverReportExtension(unittest.TestCase):
    def setUp(self):
        self.system = DeliverySystem()
        self.system.add_driver("Nima", (0, 0), "BIKE")

    def complete_one_order(self):
        order_id = self.system.create_order("BIKE", (1, 0), (4, 0))
        self.system.assign_next_order("Nima")
        self.system.update_order_status("Nima", order_id, "PICKUP")
        self.system.update_order_status("Nima", order_id, "DELIVERED")

    def test_report_for_unknown_driver(self):
        self.assertIsNone(self.system.get_driver_report("Unknown"))

    def test_report_counts_completed_orders(self):
        self.complete_one_order()
        report = self.system.get_driver_report("Nima")
        self.assertEqual(report["completed_orders"], 1)

    def test_report_contains_current_credit_and_position(self):
        self.complete_one_order()
        report = self.system.get_driver_report("Nima")
        self.assertEqual(report["credit"], Decimal("320"))
        self.assertEqual(report["position"], (4, 0))
        self.assertEqual(report["status"], "FREE")
