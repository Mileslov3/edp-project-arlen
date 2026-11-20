import unittest

from edp.event_queue import EventQueue
from edp.events import EventType as T
from edp.handlers import Handlers
from edp.producers import CustomerApp
from edp.shop import Shop


class FlowTest(unittest.TestCase):
    def setUp(self):
        self.shop, self.q = Shop(), EventQueue()
        Handlers(self.q, self.shop).register()
        self.app = CustomerApp(self.q, self.shop)
        self.seen = []
        self.q.subscribe("*", lambda e: self.seen.append(e.type))

    def test_successful_order(self):
        self.app.place_order("Anna", ["espresso"])
        self.q.run()
        self.assertIn(T.ORDER_READY, self.seen)
        self.assertEqual(self.shop.wallets["Anna"], 22)

    def test_payment_failed(self):
        self.app.place_order("Bob", ["latte"])
        self.q.run()
        self.assertIn(T.PAYMENT_FAILED, self.seen)
        self.assertNotIn(T.ORDER_READY, self.seen)

    def test_out_of_stock_refund(self):
        self.shop.stock["milk"] = 0
        self.app.place_order("Carol", ["latte"])
        self.q.run()
        self.assertIn(T.OUT_OF_STOCK, self.seen)
        self.assertIn(T.REFUND_ISSUED, self.seen)
        self.assertEqual(self.shop.wallets["Carol"], 50)


if __name__ == "__main__":
    unittest.main()
