# ☕ Coffee Shop EDP

A small **Event-Driven Programming** demo: a coffee shop where ordering, payment,
stock control, the barista and notifications communicate only through **events**
in a local event queue. No network, no external libraries.

## Requirements
- Python 3.8+ (standard library only, nothing to `pip install`)

## How to run
```bash
git clone <your-repo-url>
cd coffee-shop-edp
python main.py
```
(on some systems use `python3 main.py`)

The program runs 3 scenarios and prints every event (`[LOG]`) plus reactions of handlers:
1. **Anna** orders 2 lattes - success, loyalty points, milk gets low -> restock requested
2. **Bob** orders with too little money - `PaymentFailed`
3. **Carol** orders a latte but milk is gone - `OutOfStock` -> `RefundIssued`

## How to run tests
```bash
python -m unittest discover -s tests -t .
```

## Project structure
```
.
├── main.py              # entry point, demo scenarios
├── edp/
│   ├── events.py        # Event class + event types
│   ├── event_queue.py   # local event queue + subscribe/publish
│   ├── producers.py     # event producers
│   ├── handlers.py      # event handlers
│   └── shop.py          # menu, stock, wallets (state)
├── tests/test_flow.py   # tests
├── events.md            # list of all events
└── architecture.md      # architecture + diagrams
```

## Documentation
- [events.md](events.md) - all events and their data
- [architecture.md](architecture.md) - producers, queue, handlers
