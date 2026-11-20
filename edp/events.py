"""Event definitions. Full description of every event: see events.md."""
from dataclasses import dataclass, field
from datetime import datetime
from itertools import count

_ids = count(1)


class EventType:
    ORDER_PLACED = "OrderPlaced"
    PAYMENT_RECEIVED = "PaymentReceived"
    PAYMENT_FAILED = "PaymentFailed"
    INGREDIENTS_RESERVED = "IngredientsReserved"
    OUT_OF_STOCK = "OutOfStock"
    LOW_STOCK_DETECTED = "LowStockDetected"
    RESTOCK_REQUESTED = "RestockRequested"
    ORDER_PREPARING = "OrderPreparing"
    ORDER_READY = "OrderReady"
    REFUND_ISSUED = "RefundIssued"
    LOYALTY_POINTS_ADDED = "LoyaltyPointsAdded"


@dataclass
class Event:
    type: str
    payload: dict
    id: int = field(default_factory=lambda: next(_ids))
    timestamp: datetime = field(default_factory=datetime.now)

    def __str__(self):
        return f"#{self.id} {self.type} {self.payload}"
