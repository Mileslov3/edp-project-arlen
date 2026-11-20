"""Coffee shop - event-driven programming demo.  Run: python main.py"""
from edp.event_queue import EventQueue
from edp.handlers import Handlers
from edp.producers import CustomerApp, InventoryMonitor
from edp.shop import Shop


def main():
    shop = Shop()
    queue = EventQueue()
    Handlers(queue, shop).register()
    app = CustomerApp(queue, shop)
    monitor = InventoryMonitor(queue, shop)

    scenarios = [
        ("Anna orders 2 lattes (should succeed)", "Anna", ["latte", "latte"]),
        ("Bob orders a cappuccino with too little money", "Bob", ["cappuccino"]),
        ("Carol orders a latte but milk ran out", "Carol", ["latte"]),
    ]
    for title, customer, items in scenarios:
        print(f"\n=== {title} ===")
        app.place_order(customer, items)
        queue.run()
        monitor.check()      # periodic stock check (producer)
        queue.run()

    print("\n=== Final state ===")
    print("Stock:   ", shop.stock)
    print("Wallets: ", shop.wallets)
    print("Loyalty: ", shop.loyalty)


if __name__ == "__main__":
    main()
