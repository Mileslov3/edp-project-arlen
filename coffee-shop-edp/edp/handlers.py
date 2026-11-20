"""Event handlers - they REACT to events (and may publish new ones)."""
from .events import EventType as T


class Handlers:
    def __init__(self, queue, shop):
        self.q, self.shop = queue, shop
        self._low_stock_reported = set()

    def register(self):
        s = self.q.subscribe
        s("*", self.log_event)
        s(T.ORDER_PLACED, self.process_payment)
        s(T.PAYMENT_RECEIVED, self.reserve_ingredients)
        s(T.PAYMENT_FAILED, self.notify_payment_failed)
        s(T.INGREDIENTS_RESERVED, self.start_preparing)
        s(T.ORDER_PREPARING, self.prepare_drink)
        s(T.ORDER_READY, self.notify_order_ready)
        s(T.ORDER_READY, self.add_loyalty_points)
        s(T.OUT_OF_STOCK, self.refund_customer)
        s(T.REFUND_ISSUED, self.notify_refund)
        s(T.LOW_STOCK_DETECTED, self.request_restock)

    # --- logging (listens to ALL events) ---
    def log_event(self, e):
        print(f"  [LOG] {e}")

    # --- payment ---
    def process_payment(self, e):
        p = e.payload
        if self.shop.wallets[p["customer"]] >= p["total"]:
            self.shop.wallets[p["customer"]] -= p["total"]
            self.q.publish(T.PAYMENT_RECEIVED, p)
        else:
            self.q.publish(T.PAYMENT_FAILED, {**p, "reason": "not enough money"})

    def notify_payment_failed(self, e):
        p = e.payload
        print(f"  [NOTIFY] {p['customer']}: order #{p['order_id']} rejected ({p['reason']})")

    # --- inventory ---
    def reserve_ingredients(self, e):
        p = e.payload
        needed = self.shop.order_ingredients(p["items"])
        missing = [i for i, a in needed.items() if self.shop.stock[i] < a]
        if missing:
            self.q.publish(T.OUT_OF_STOCK, {**p, "missing": missing})
            return
        for ing, amount in needed.items():
            self.shop.stock[ing] -= amount
        self.q.publish(T.INGREDIENTS_RESERVED, p)

    def request_restock(self, e):
        ing = e.payload["ingredient"]
        if ing in self._low_stock_reported:
            return
        self._low_stock_reported.add(ing)
        self.q.publish(T.RESTOCK_REQUESTED, {"ingredient": ing, "amount": 100})

    # --- barista ---
    def start_preparing(self, e):
        self.q.publish(T.ORDER_PREPARING, e.payload)

    def prepare_drink(self, e):
        print(f"  [BARISTA] making order #{e.payload['order_id']}: {', '.join(e.payload['items'])}")
        self.q.publish(T.ORDER_READY, e.payload)

    def notify_order_ready(self, e):
        p = e.payload
        print(f"  [NOTIFY] {p['customer']}: your order #{p['order_id']} is ready!")

    def add_loyalty_points(self, e):
        p = e.payload
        points = p["total"] // 5
        self.shop.loyalty[p["customer"]] = self.shop.loyalty.get(p["customer"], 0) + points
        self.q.publish(T.LOYALTY_POINTS_ADDED, {"customer": p["customer"], "points": points})

    # --- refunds ---
    def refund_customer(self, e):
        p = e.payload
        self.shop.wallets[p["customer"]] += p["total"]
        self.q.publish(T.REFUND_ISSUED, {"order_id": p["order_id"],
                                         "customer": p["customer"],
                                         "amount": p["total"],
                                         "missing": p["missing"]})

    def notify_refund(self, e):
        p = e.payload
        print(f"  [NOTIFY] {p['customer']}: sorry, no {', '.join(p['missing'])}. "
              f"Refunded {p['amount']} PLN for order #{p['order_id']}")
