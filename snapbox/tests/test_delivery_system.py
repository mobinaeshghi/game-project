import unittest
from decimal import Decimal

from delivery_system import DeliverySystem


class TestDeliverySystem(unittest.TestCase):
    def setUp(self):
        self.system = DeliverySystem()

    def test_empty_system(self):
        self.assertEqual(self.system.total_drivers, 0)
        self.assertEqual(self.system.company_credit, Decimal("0"))

    def test_add_driver(self):
        self.assertTrue(self.system.add_driver("Ali", (0, 0), "BIKE"))
        self.assertEqual(self.system.total_drivers, 1)

    def test_duplicate_driver_does_not_increase_count(self):
        self.system.add_driver("Ali", (0, 0), "BIKE")
        self.assertFalse(self.system.add_driver("Ali", (2, 2), "VAN"))
        self.assertEqual(self.system.total_drivers, 1)

    def test_create_order_ids_are_sequential(self):
        first = self.system.create_order("BIKE", (0, 0), (1, 1))
        second = self.system.create_order("VAN", (2, 2), (3, 3))
        self.assertEqual((first, second), (1, 2))

    def test_equal_positions_do_not_consume_id(self):
        self.assertIsNone(self.system.create_order("BIKE", (1, 1), (1, 1)))
        self.assertEqual(
            self.system.create_order("BIKE", (0, 0), (1, 0)), 1
        )

    def test_order_cost_includes_new_pending_order(self):
        order_id = self.system.create_order("BIKE", (0, 0), (2, 0))
        self.assertEqual(self.system.get_order(order_id)[2], Decimal("300"))

    def test_assign_nearest_compatible_order(self):
        self.system.add_driver("Ali", (0, 0), "BIKE")
        self.system.create_order("BIKE", (8, 8), (9, 9))
        nearer = self.system.create_order("BIKE", (1, 0), (2, 0))
        self.assertEqual(self.system.assign_next_order("Ali"), nearer)

    def test_assign_busy_driver_raises(self):
        self.system.add_driver("Ali", (0, 0), "BIKE")
        self.system.create_order("BIKE", (1, 0), (2, 0))
        self.system.assign_next_order("Ali")
        with self.assertRaises(RuntimeError):
            self.system.assign_next_order("Ali")

    def test_assign_unknown_driver_raises(self):
        with self.assertRaises(KeyError):
            self.system.assign_next_order("Missing")

    def test_order_lifecycle_and_payment(self):
        self.system.add_driver("Ali", (0, 0), "BIKE")
        order_id = self.system.create_order("BIKE", (1, 0), (3, 0))
        cost = self.system.get_order(order_id)[2]
        self.system.assign_next_order("Ali")
        self.assertTrue(self.system.update_order_status("Ali", order_id, "PICKUP"))
        self.assertTrue(self.system.update_order_status("Ali", order_id, "DELIVERED"))
        self.assertEqual(self.system.get_driver("Ali")[1], (3, 0))
        self.assertEqual(self.system.get_driver("Ali")[2], cost * Decimal("0.8"))
        self.assertEqual(self.system.get_company_credit(), cost * Decimal("0.2"))
        self.assertEqual(self.system.get_driver("Ali")[0], "FREE")

    def test_invalid_transition_does_not_change_state(self):
        self.system.add_driver("Ali", (0, 0), "BIKE")
        order_id = self.system.create_order("BIKE", (1, 0), (2, 0))
        self.system.assign_next_order("Ali")
        before = self.system.get_driver("Ali")
        self.assertFalse(self.system.update_order_status("Ali", order_id, "DELIVERED"))
        self.assertEqual(self.system.get_driver("Ali"), before)

    def test_order_history_keeps_assigned_driver(self):
        self.system.add_driver("Ali", (0, 0), "BIKE")
        order_id = self.system.create_order("BIKE", (1, 0), (2, 0))
        self.system.assign_next_order("Ali")
        self.system.update_order_status("Ali", order_id, "PICKUP")
        self.system.update_order_status("Ali", order_id, "DELIVERED")
        self.assertEqual(self.system.get_order(order_id)[1], "Ali")

    def test_near_drivers_only_returns_free(self):
        self.system.add_driver("Ali", (1, 0), "BIKE")
        self.system.add_driver("Sara", (2, 0), "BIKE")
        self.system.create_order("BIKE", (0, 0), (1, 0))
        self.system.assign_next_order("Ali")
        self.assertEqual(self.system.get_near_drivers((0, 0), 5), ["Sara"])

    def test_count_orders_includes_all_statuses(self):
        self.system.add_driver("Ali", (0, 0), "BIKE")
        order_id = self.system.create_order("BIKE", (1, 0), (2, 0))
        self.system.assign_next_order("Ali")
        self.assertEqual(self.system.count_orders((0, 0), 1, "START"), 1)
        self.system.update_order_status("Ali", order_id, "PICKUP")
        self.assertEqual(self.system.count_orders((0, 0), 1, "START"), 1)

    def test_nearest_pending_order(self):
        first = self.system.create_order("BIKE", (5, 0), (6, 0))
        self.system.create_order("VAN", (1, 0), (2, 0))
        self.assertEqual(self.system.get_nearest_pending_order((0, 0)), 2)

    def test_get_unknown_entities(self):
        self.assertIsNone(self.system.get_driver("Nobody"))
        self.assertIsNone(self.system.get_order(999))

    def test_read_only_system_properties(self):
        with self.assertRaises(AttributeError):
            self.system.company_credit = Decimal("10")
        with self.assertRaises(AttributeError):
            self.system.total_drivers = 10
