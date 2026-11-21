"""کلاس سفارش."""

from helpers import (
    validate_category,
    validate_money,
    validate_positive_int,
    validate_position,
)


class Order:
    def __init__(
        self,
        order_id,
        service_category,
        starting_position,
        finishing_position,
        cost,
    ):
        self._order_id = validate_positive_int(order_id, "order_id")
        self._service_category = validate_category(service_category)
        self._starting_position = validate_position(starting_position)
        self._finishing_position = validate_position(finishing_position)
        self._cost = validate_money(cost, "cost")
        self._status = "PENDING"
        self._assigned_driver = None

    @property
    def order_id(self):
        return self._order_id

    @property
    def service_category(self):
        return self._service_category

    @property
    def starting_position(self):
        return self._starting_position

    @property
    def finishing_position(self):
        return self._finishing_position

    @property
    def cost(self):
        return self._cost

    @property
    def status(self):
        return self._status

    @property
    def assigned_driver(self):
        return self._assigned_driver

    def is_pending(self):
        return self._status == "PENDING"

    def _change_status(self, status):
        self._status = status

    def _set_assigned_driver(self, driver):
        self._assigned_driver = driver
