def distance(a, b):
    # فاصله Manhattan
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def pos_text(p):
    return "(%d, %d)" % (p[0], p[1])


class Driver:
    def __init__(self, username, position, category):
        self.username = username
        self.position = position
        self.category = category
        self.credit = 0
        self.status = "FREE"
        self.order = None  # آخرین سفارش تخصیص‌یافته به راننده


class Order:
    def __init__(self, order_id, category, start, finish, cost):
        self.order_id = order_id
        self.category = category
        self.start = start
        self.finish = finish
        self.cost = cost
        self.status = "PENDING"
        self.driver = None


class System:
    def __init__(self):
        self.drivers = {}   # نام -> راننده (ترتیب ثبت حفظ می‌شود)
        self.orders = []    # سفارش شماره n در خانه n-1
        self.company = 0

    def add_driver(self, username, position, category):
        if username in self.drivers:
            return "user previously added"
        self.drivers[username] = Driver(username, position, category)
        return "user added successfully"

    def create_order(self, category, start, finish):
        if start == finish:
            return "invalid order"
        k = 1  # خود سفارش جدید
        for o in self.orders:
            if o.status == "PENDING" and o.category == category:
                k += 1
        cost = (k + distance(start, finish)) * 100
        order = Order(len(self.orders) + 1, category, start, finish, cost)
        self.orders.append(order)
        return str(order.order_id)

    def nearest_pending(self, position, category=None):
        best = None
        best_dist = 0
        for o in self.orders:
            if o.status != "PENDING":
                continue
            if category is not None and o.category != category:
                continue
            d = distance(position, o.start)
            if best is None or d < best_dist:  # در تساوی، قدیمی‌تر می‌ماند
                best = o
                best_dist = d
        return best

    def assign_next_order(self, username):
        if username not in self.drivers:
            return "invalid driver name"
        driver = self.drivers[username]
        if driver.status == "BUSY":
            return "driver is already busy"
        order = self.nearest_pending(driver.position, driver.category)
        if order is None:
            return "there is no order right now"
        order.status = "ARRIVED"
        order.driver = driver
        driver.status = "BUSY"
        driver.order = order
        return "%d assigned to %s" % (order.order_id, username)

    def get_driver(self, username):
        if username not in self.drivers:
            return "invalid driver name"
        d = self.drivers[username]
        return "%s %s %d" % (d.status, pos_text(d.position), d.credit)

    def order_update(self, status, username, order_id):
        if username not in self.drivers:
            return "invalid driver name"
        driver = self.drivers[username]
        if driver.order is None or driver.order.order_id != order_id:
            return "wrong order-id"
        order = driver.order
        if order.status == "ARRIVED" and status == "PICKUP":
            order.status = "PICKUP"
            driver.position = order.start
        elif order.status == "PICKUP" and status == "DELIVERED":
            order.status = "DELIVERED"
            driver.position = order.finish
            driver.status = "FREE"
            driver.credit += order.cost * 80 // 100
            self.company += order.cost - order.cost * 80 // 100
        else:
            return "invalid status"
        return "status changed successfully"

    def get_order(self, order_id):
        if order_id < 1 or order_id > len(self.orders):
            return "invalid order"
        o = self.orders[order_id - 1]
        name = "None"
        if o.driver is not None:
            name = o.driver.username
        return "%s %s %d" % (o.status, name, o.cost)

    def get_order_list(self, status):
        ids = [str(o.order_id) for o in self.orders if o.status == status]
        return " ".join(ids) if ids else "None"

    def get_driver_list(self, status):
        names = [d.username for d in self.drivers.values() if d.status == status]
        return " ".join(names) if names else "None"

    def get_near_driver(self, position, count):
        free = [d for d in self.drivers.values() if d.status == "FREE"]
        free.sort(key=lambda d: distance(position, d.position))  # sort پایدار است
        names = [d.username for d in free[:count]]
        return " ".join(names) if names else "None"

    def get_cnt_order(self, position, dist, endpoint):
        total = 0
        for o in self.orders:
            point = o.start if endpoint == "START" else o.finish
            if distance(position, point) <= dist:
                total += 1
        return str(total)

    def get_nearest_pending_order(self, position):
        order = self.nearest_pending(position)
        return "None" if order is None else str(order.order_id)

    def get_company(self):
        return str(self.company)


def parse_pos(text):
    x, y = text.split(",")
    return (int(x), int(y))


def main():
    system = System()
    while True:
        try:
            line = input().strip()
        except EOFError:
            break
        if line == "END":
            break
        if line == "":
            continue
        # "(12, 5)" را به "12,5" تبدیل می‌کنیم تا با split جدا نشود
        line = line.replace("(", "").replace(")", "").replace(", ", ",")
        p = line.split()
        cmd = p[0]
        if cmd == "ADD-DRIVER":
            print(system.add_driver(p[1], parse_pos(p[2]), p[3]))
        elif cmd == "CREATE-ORDER":
            print(system.create_order(p[1], parse_pos(p[2]), parse_pos(p[3])))
        elif cmd == "ASSIGN-NEXT-ORDER":
            print(system.assign_next_order(p[1]))
        elif cmd == "GET-DRIVER":
            print(system.get_driver(p[1]))
        elif cmd == "ORDER-UPDATE":
            print(system.order_update(p[1], p[2], int(p[3])))
        elif cmd == "GET-ORDER":
            print(system.get_order(int(p[1])))
        elif cmd == "GET-ORDER-LIST":
            print(system.get_order_list(p[1]))
        elif cmd == "GET-DRIVER-LIST":
            print(system.get_driver_list(p[1]))
        elif cmd == "GET-NEAR-DRIVER":
            print(system.get_near_driver(parse_pos(p[1]), int(p[2])))
        elif cmd == "GET-CNT-ORDER":
            print(system.get_cnt_order(parse_pos(p[1]), int(p[2]), p[3]))
        elif cmd == "GET-NEAREST-PENDING-ORDER":
            print(system.get_nearest_pending_order(parse_pos(p[1])))
        elif cmd == "GET-COMPANY":
            print(system.get_company())


main()
