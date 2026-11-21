import unittest
from decimal import Decimal

from order import Order


class TestOrder(unittest.TestCase):
    def make_order(self):
        return Order(1, "VAN", (1, 2), (3, 4), Decimal("500"))

    def test_initial_values(self):
        order = self.make_order()
        self.assertEqual(order.order_id, 1)
        self.assertEqual(order.status, "PENDING")
        self.assertIsNone(order.assigned_driver)
        self.assertTrue(order.is_pending())

    def test_cost_must_be_decimal(self):
        with self.assertRaises(TypeError):
            Order(1, "VAN", (1, 2), (3, 4), 500)

    def test_cost_must_be_positive(self):
        with self.assertRaises(ValueError):
            Order(1, "VAN", (1, 2), (3, 4), Decimal("0"))

    def test_order_id_must_be_positive(self):
        with self.assertRaises(ValueError):
            Order(0, "VAN", (1, 2), (3, 4), Decimal("500"))

    def test_read_only_status(self):
        order = self.make_order()
        with self.assertRaises(AttributeError):
            order.status = "DELIVERED"
