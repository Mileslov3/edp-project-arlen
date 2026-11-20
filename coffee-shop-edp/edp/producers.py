"""Event producers - they only CREATE events and put them in the queue."""
from .events import EventType
from .shop import LOW_STOCK_THRESHOLD


class CustomerApp:
    """Producer: customer's mobile app. Emits OrderPlaced."""

    def __init__(self, queue, shop):
        self.queue, self.shop = queue, shop
        self._next_order = 1

    def place_order(self, customer, items):
        order_id = self._next_order
        self._next_order += 1
        self.queue.publish(EventType.ORDER_PLACED, {
            "order_id": order_id,
            "customer": customer,
            "items": items,
            "total": self.shop.order_price(items),
        })
        return order_id


class InventoryMonitor:
    """Producer: periodic stock check. Emits LowStockDetected."""

    def __init__(self, queue, shop):
        self.queue, self.shop = queue, shop

    def check(self):
        for ingredient, amount in self.shop.stock.items():
            if amount < LOW_STOCK_THRESHOLD[ingredient]:
                self.queue.publish(EventType.LOW_STOCK_DETECTED,
                                   {"ingredient": ingredient, "left": amount})
