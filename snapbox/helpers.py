"""توابع کمکی برای اعتبارسنجی و محاسبه فاصله."""

import re
from decimal import Decimal

categories = ("BIKE", "VAN", "TRUCK")
driver_statuses = ("FREE", "BUSY")
order_statuses = ("PENDING", "ARRIVED", "PICKUP", "DELIVERED")
endpoints = ("START", "FINISH")

_username_pattern = re.compile(r"[A-Za-z0-9]{1,25}")


def is_int(value):
    """بررسی عدد صحیح، بدون پذیرفتن bool."""
    return isinstance(value, int) and not isinstance(value, bool)


def validate_position(position):
    if not isinstance(position, tuple):
        raise TypeError("position must be a tuple")
    if len(position) != 2:
        raise ValueError("position must contain exactly two values")
    if not all(is_int(item) for item in position):
        raise TypeError("position coordinates must be integers")
    return position


def validate_choice(value, allowed, name):
    if not isinstance(value, str):
        raise TypeError("%s must be str" % name)
    if value not in allowed:
        raise ValueError("invalid %s" % name)
    return value


def validate_category(value):
    return validate_choice(value, categories, "service_category")


def validate_username(value):
    if not isinstance(value, str):
        raise TypeError("username must be str")
    if not _username_pattern.fullmatch(value):
        raise ValueError("invalid username")
    return value


def validate_positive_int(value, name):
    if not is_int(value):
        raise TypeError("%s must be int" % name)
    if value <= 0:
        raise ValueError("%s must be positive" % name)
    return value


def validate_non_negative_int(value, name):
    if not is_int(value):
        raise TypeError("%s must be int" % name)
    if value < 0:
        raise ValueError("%s must not be negative" % name)
    return value


def validate_money(value, name):
    if not isinstance(value, Decimal):
        raise TypeError("%s must be Decimal" % name)
    if not value.is_finite() or value <= 0:
        raise ValueError("%s must be positive and finite" % name)
    return value


def manhattan(first, second):
    validate_position(first)
    validate_position(second)
    return abs(first[0] - second[0]) + abs(first[1] - second[1])


def format_position(position):
    return "(%d, %d)" % position


def format_money(value):
    """برای خروجی CLI، Decimal صحیح را بدون پسوند .0 چاپ می‌کند."""
    return str(value.quantize(Decimal("1"))) if value == value.to_integral_value() else str(value)
