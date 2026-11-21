"""رابط خط فرمان مطابق دستورهای پروژه و مسئله کوئرا."""

import re

from delivery_system import DeliverySystem
from helpers import format_money, format_position


def split_command(line):
    return re.findall(r"\([^)]*\)|\S+", line.strip())


def parse_position(token):
    match = re.fullmatch(r"\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)", token)
    if match is None:
        raise ValueError("invalid position format")
    return (int(match.group(1)), int(match.group(2)))


def run():
    system = DeliverySystem()

    while True:
        line = input().strip()
        if not line:
            continue

        parts = split_command(line)
        command = parts[0]

        if command == "END":
            break

        try:
            if command == "ADD-DRIVER":
                _, username, position, category = parts
                result = system.add_driver(
                    username, parse_position(position), category
                )
                print(
                    "user added successfully"
                    if result else "user previously added"
                )

            elif command == "CREATE-ORDER":
                _, category, start, finish = parts
                order_id = system.create_order(
                    category, parse_position(start), parse_position(finish)
                )
                print("invalid order" if order_id is None else order_id)

            elif command == "ASSIGN-NEXT-ORDER":
                _, username = parts
                order_id = system.assign_next_order(username)
                if order_id is None:
                    print("there is no order right now")
                else:
                    print("%d assigned to %s" % (order_id, username))

            elif command == "GET-DRIVER":
                _, username = parts
                result = system.get_driver(username)
                if result is None:
                    print("invalid driver name")
                else:
                    status, position, credit = result
                    print("%s %s %s" % (
                        status, format_position(position), format_money(credit)
                    ))

            elif command == "ORDER-UPDATE":
                _, new_status, username, order_id = parts
                driver_info = system.get_driver(username)
                if driver_info is None:
                    print("invalid driver name")
                else:
                    order_info = system.get_order(int(order_id))
                    if order_info is None or order_info[1] != username:
                        print("wrong order-id")
                    elif system.update_order_status(username, int(order_id), new_status):
                        print("status changed successfully")
                    else:
                        print("wrong order-id" if order_info[0] == "DELIVERED" else "invalid status")

            elif command == "GET-ORDER":
                _, order_id = parts
                result = system.get_order(int(order_id))
                if result is None:
                    print("invalid order")
                else:
                    status, username, cost = result
                    print("%s %s %s" % (status, username, format_money(cost)))

            elif command == "GET-ORDER-LIST":
                _, status = parts
                result = system.get_order_list(status)
                print(" ".join(map(str, result)) if result else "None")

            elif command == "GET-DRIVER-LIST":
                _, status = parts
                result = system.get_driver_list(status)
                print(" ".join(result) if result else "None")

            elif command == "GET-NEAR-DRIVER":
                _, position, count = parts
                result = system.get_near_drivers(
                    parse_position(position), int(count)
                )
                print(" ".join(result) if result else "None")

            elif command == "GET-CNT-ORDER":
                _, position, distance, endpoint = parts
                print(system.count_orders(
                    parse_position(position), int(distance), endpoint
                ))

            elif command == "GET-NEAREST-PENDING-ORDER":
                _, position = parts
                result = system.get_nearest_pending_order(parse_position(position))
                print("None" if result is None else result)

            elif command == "GET-COMPANY":
                print(format_money(system.get_company_credit()))

            else:
                print("invalid command")

        except KeyError:
            print("invalid driver name")
        except (TypeError, ValueError, IndexError):
            print("invalid input")
        except RuntimeError:
            print("driver is already busy")


if __name__ == "__main__":
    run()
