"""کلاس راننده."""

from decimal import Decimal

from helpers import validate_category, validate_position, validate_username


class Driver:
    def __init__(self, username, position, service_category):
        self._username = validate_username(username)
        self._position = validate_position(position)
        self._service_category = validate_category(service_category)
        self._credit = Decimal("0")
        self._status = "FREE"
        self._current_order = None

    @property
    def username(self):
        return self._username

    @property
    def position(self):
        return self._position

    @property
    def service_category(self):
        return self._service_category

    @property
    def credit(self):
        return self._credit

    @property
    def status(self):
        return self._status

    @property
    def current_order(self):
        return self._current_order

    def is_available(self):
        return self._status == "FREE"

    def _change_position(self, position):
        self._position = validate_position(position)

    def _change_status(self, status):
        if status not in ("FREE", "BUSY"):
            raise ValueError("invalid driver status")
        self._status = status

    def _set_current_order(self, order):
        self._current_order = order

    def _add_credit(self, amount):
        if not isinstance(amount, Decimal):
            raise TypeError("credit amount must be Decimal")
        if not amount.is_finite() or amount < 0:
            raise ValueError("credit amount must be non-negative and finite")
        self._credit += amount
