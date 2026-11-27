"""منطق اصلی سامانه مدیریت سفارش‌ها."""

from decimal import Decimal

from driver import Driver
from order import Order
from helpers import (
    endpoints,
    order_statuses,
    manhattan,
    validate_category,
    validate_choice,
    validate_non_negative_int,
    validate_position,
    validate_positive_int,
    validate_username,
)


class DeliverySystem:
    def __init__(self):
        self._drivers = {}
        self._orders = {}
        self._next_order_id = 1
        self._company_credit = Decimal("0")

    @property
    def company_credit(self):
        return self._company_credit

    @property
    def total_drivers(self):
        return len(self._drivers)

    def add_driver(self, username, position, service_category):
        #اگ از اینیت استفاده میکردیم تعداد راننده ها ثابت میشد
        username = validate_username(username)
        position = validate_position(position)
        service_category = validate_category(service_category)

        if username in self._drivers:
            return False

        self._drivers[username] = Driver(username, position, service_category)
        return True

    def create_order(self, service_category, starting_position, finishing_position):
        service_category = validate_category(service_category)
        starting_position = validate_position(starting_position)
        finishing_position = validate_position(finishing_position)

        if starting_position == finishing_position:
            return None

        pending_count = 0
        for order in self._orders.values():
            if order.service_category == service_category and order.is_pending():
              pending_count += 1
         distance = manhattan(starting_position, finishing_position)
        cost = Decimal("100") * Decimal(pending_count + 1 + distance)

        order_id = self._next_order_id
        order = Order(
            order_id,
            service_category,
            starting_position,
            finishing_position,
            cost,
        )
        self._orders[order_id] = order
        self._next_order_id += 1
        return order_id

    def assign_next_order(self, username):
        username = validate_username(username)
        if username not in self._drivers:
            raise KeyError(username)

        driver = self._drivers[username]
        if not driver.is_available():
            raise RuntimeError("driver is busy")

        candidates = [
            order
            for order in self._orders.values()
            if order.is_pending()
            and order.service_category == driver.service_category
        ]
        if not candidates:
            return None

        selected = min(
            candidates,
            key=lambda order: manhattan(driver.position, order.starting_position),
        )
        selected._change_status("ARRIVED")
        selected._set_assigned_driver(driver)
        driver._set_current_order(selected)
        driver._change_status("BUSY")
        return selected.order_id

    def update_order_status(self, username, order_id, new_status):
        username = validate_username(username)
        order_id = validate_positive_int(order_id, "order_id")
        new_status = validate_choice(new_status, order_statuses, "new_status")

        if username not in self._drivers:
            raise KeyError(username)

        driver = self._drivers[username]
        order = self._orders.get(order_id)

        if order is None or driver.current_order is not order:
            return False

        if order.assigned_driver is not driver:
            return False

        if order.status == "ARRIVED" and new_status == "PICKUP":
            order._change_status("PICKUP")
            driver._change_position(order.starting_position)
            return True

        if order.status == "PICKUP" and new_status == "DELIVERED":
            order._change_status("DELIVERED")
            driver._change_position(order.finishing_position)
            driver._add_credit(order.cost * Decimal("0.8"))
            self._company_credit += order.cost * Decimal("0.2")
            driver._change_status("FREE")
            driver._set_current_order(None)
            return True

        return False

    def get_driver(self, username):
        username = validate_username(username)
        driver = self._drivers.get(username)
        if driver is None:
            return None
        return (driver.status, driver.position, driver.credit)

    def get_order(self, order_id):
        order_id = validate_positive_int(order_id, "order_id")
        order = self._orders.get(order_id)
        if order is None:
            return None
        assigned_username = (
            order.assigned_driver.username if order.assigned_driver is not None else None
        )
        return (order.status, assigned_username, order.cost)

    def get_order_list(self, status):
        status = validate_choice(status, order_statuses, "status")
        return [
            order.order_id
            for order in self._orders.values()
            if order.status == status
        ]

    def get_driver_list(self, status):
        status = validate_choice(status, ("FREE", "BUSY"), "status")
        return [
            driver.username
            for driver in self._drivers.values()
            if driver.status == status
        ]

    def get_near_drivers(self, position, count):
        position = validate_position(position)
        count = validate_non_negative_int(count, "count")
        available = [
            driver for driver in self._drivers.values() if driver.is_available()
        ]
        available.sort(key=lambda driver: manhattan(position, driver.position))
        return [driver.username for driver in available[:count]]

    def count_orders(self, position, distance, endpoint):
        position = validate_position(position)
        distance = validate_non_negative_int(distance, "distance")
        endpoint = validate_choice(endpoint, endpoints, "endpoint")

        total = 0
        for order in self._orders.values():
            target = (
                order.starting_position if endpoint == "START"
                else order.finishing_position
            )
            if manhattan(position, target) <= distance:
                total += 1
        return total

    def get_nearest_pending_order(self, position):
        position = validate_position(position)
        pending = [order for order in self._orders.values() if order.is_pending()]
        if not pending:
            return None
        nearest = min(
            pending,
            key=lambda order: manhattan(position, order.starting_position),
        )
        return nearest.order_id

    def get_company_credit(self):
        return self._company_credit

    def get_driver_report(self, username):
        """قابلیت افزوده: گزارش خلاصه عملکرد راننده."""
        username = validate_username(username)
        driver = self._drivers.get(username)
        if driver is None:
            return None

        delivered_orders = [
            order
            for order in self._orders.values()
            if order.assigned_driver is driver and order.status == "DELIVERED"
        ]
        return {
            "username": driver.username,
            "completed_orders": len(delivered_orders),
            "credit": driver.credit,
            "status": driver.status,
            "position": driver.position,
        }
