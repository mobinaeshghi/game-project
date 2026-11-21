import unittest
from decimal import Decimal

from driver import Driver


class TestDriver(unittest.TestCase):
    def test_initial_values(self):
        driver = Driver("Ali123", (1, 2), "BIKE")
        self.assertEqual(driver.username, "Ali123")
        self.assertEqual(driver.position, (1, 2))
        self.assertEqual(driver.service_category, "BIKE")
        self.assertEqual(driver.credit, Decimal("0"))
        self.assertEqual(driver.status, "FREE")
        self.assertIsNone(driver.current_order)

    def test_is_available_when_free(self):
        self.assertTrue(Driver("Ali", (0, 0), "VAN").is_available())

    def test_username_wrong_type(self):
        with self.assertRaises(TypeError):
            Driver(123, (0, 0), "BIKE")

    def test_username_bad_format(self):
        with self.assertRaises(ValueError):
            Driver("ali-name", (0, 0), "BIKE")

    def test_position_wrong_type(self):
        with self.assertRaises(TypeError):
            Driver("Ali", [0, 0], "BIKE")

    def test_position_wrong_length(self):
        with self.assertRaises(ValueError):
            Driver("Ali", (0, 0, 1), "BIKE")

    def test_bool_coordinate_rejected(self):
        with self.assertRaises(TypeError):
            Driver("Ali", (True, 0), "BIKE")

    def test_invalid_category(self):
        with self.assertRaises(ValueError):
            Driver("Ali", (0, 0), "CAR")

    def test_read_only_credit(self):
        driver = Driver("Ali", (0, 0), "BIKE")
        with self.assertRaises(AttributeError):
            driver.credit = Decimal("50")
