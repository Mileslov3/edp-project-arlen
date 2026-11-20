# Events

All events are defined in `edp/events.py`. Every event has: `id`, `type`, `timestamp`, `payload`.

| # | Event | Published by | Handled by | When it happens |
|---|-------|--------------|------------|-----------------|
| 1 | `OrderPlaced` | CustomerApp (producer) | `process_payment` | Customer sends an order |
| 2 | `PaymentReceived` | `process_payment` | `reserve_ingredients` | Customer had enough money, it was charged |
| 3 | `PaymentFailed` | `process_payment` | `notify_payment_failed` | Not enough money |
| 4 | `IngredientsReserved` | `reserve_ingredients` | `start_preparing` | All ingredients in stock, taken from it |
| 5 | `OutOfStock` | `reserve_ingredients` | `refund_customer` | Some ingredient is missing |
| 6 | `OrderPreparing` | `start_preparing` | `prepare_drink` | Barista starts the drink |
| 7 | `OrderReady` | `prepare_drink` | `notify_order_ready`, `add_loyalty_points` | Drink is ready |
| 8 | `RefundIssued` | `refund_customer` | `notify_refund` | Money returned after OutOfStock |
| 9 | `LoyaltyPointsAdded` | `add_loyalty_points` | (only logger) | Points given for finished order |
| 10 | `LowStockDetected` | InventoryMonitor (producer) | `request_restock` | Ingredient below threshold |
| 11 | `RestockRequested` | `request_restock` | (only logger) | Ordering new supplies |

The `log_event` handler subscribes to `*` and receives **every** event.

## Payloads

| Event | Payload |
|-------|---------|
| `OrderPlaced` | `order_id`, `customer`, `items` (list), `total` |
| `PaymentReceived` | same as `OrderPlaced` |
| `PaymentFailed` | same as `OrderPlaced` + `reason` |
| `IngredientsReserved` | same as `OrderPlaced` |
| `OutOfStock` | same as `OrderPlaced` + `missing` (list of ingredients) |
| `OrderPreparing` | same as `OrderPlaced` |
| `OrderReady` | same as `OrderPlaced` |
| `RefundIssued` | `order_id`, `customer`, `amount`, `missing` |
| `LoyaltyPointsAdded` | `customer`, `points` |
| `LowStockDetected` | `ingredient`, `left` |
| `RestockRequested` | `ingredient`, `amount` |
