# Architecture

The app uses **Event-Driven Architecture**. Components do not call each other directly.
Producers put events in a queue, and handlers subscribed to those events react to them.
A handler can publish new events, which creates a chain of reactions.

## Components

### 1. Event producers (`edp/producers.py`)
They only create events and put them in the queue.
- **CustomerApp** - emits `OrderPlaced`
- **InventoryMonitor** - periodically checks stock, emits `LowStockDetected`

### 2. Event queue (`edp/event_queue.py`)
Local FIFO queue (`collections.deque`) + a dictionary `event type -> list of handlers`.
- `subscribe(type, handler)` - register a handler
- `publish(type, payload)` - add an event to the queue
- `run()` - take events one by one and call all subscribed handlers, until the queue is empty

### 3. Event handlers (`edp/handlers.py`)
Functions that react to events: payment, inventory, barista, notifications,
loyalty, refunds, logging. Some of them publish follow-up events.

## Diagram

```mermaid
flowchart LR
    subgraph Producers
        P1[CustomerApp]
        P2[InventoryMonitor]
    end

    Q[(Event Queue)]

    subgraph Handlers
        H1[process_payment]
        H2[reserve_ingredients]
        H3[start_preparing / prepare_drink]
        H4[notify_order_ready]
        H5[add_loyalty_points]
        H6[refund_customer]
        H7[request_restock]
        H8[notify_*]
        H9[log_event - all events]
    end

    P1 -- OrderPlaced --> Q
    P2 -- LowStockDetected --> Q
    Q --> H1
    H1 -- PaymentReceived / PaymentFailed --> Q
    Q --> H2
    H2 -- IngredientsReserved / OutOfStock --> Q
    Q --> H3
    H3 -- OrderPreparing / OrderReady --> Q
    Q --> H4
    Q --> H5
    Q --> H6
    H6 -- RefundIssued --> Q
    Q --> H7
    H7 -- RestockRequested --> Q
    Q --> H8
    Q --> H9
```

## Event flow (successful order)

```mermaid
sequenceDiagram
    participant C as CustomerApp
    participant Q as EventQueue
    participant H as Handlers
    C->>Q: OrderPlaced
    Q->>H: process_payment
    H->>Q: PaymentReceived
    Q->>H: reserve_ingredients
    H->>Q: IngredientsReserved
    Q->>H: start_preparing
    H->>Q: OrderPreparing
    Q->>H: prepare_drink
    H->>Q: OrderReady
    Q->>H: notify_order_ready, add_loyalty_points
    H->>Q: LoyaltyPointsAdded
```

## Failure branches
- `OrderPlaced` -> `PaymentFailed` -> customer notification (end)
- `PaymentReceived` -> `OutOfStock` -> `RefundIssued` -> customer notification
- stock below threshold -> `LowStockDetected` -> `RestockRequested`

## Why this design
- **Loose coupling**: the payment code does not know about the barista or notifications.
- **Easy to extend**: a new feature = a new handler with one `subscribe` line.
- **Easy to test**: publish an event and check which events appear next.
