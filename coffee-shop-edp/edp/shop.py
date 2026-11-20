"""Shared state of the coffee shop (menu, stock, customer wallets)."""

MENU = {
    "espresso":   {"price": 8,  "ingredients": {"coffee_beans": 8}},
    "latte":      {"price": 12, "ingredients": {"coffee_beans": 8, "milk": 20}},
    "cappuccino": {"price": 11, "ingredients": {"coffee_beans": 8, "milk": 12}},
}

LOW_STOCK_THRESHOLD = {"coffee_beans": 20, "milk": 15}


class Shop:
    def __init__(self):
        self.stock = {"coffee_beans": 100, "milk": 50}
        self.wallets = {"Anna": 30, "Bob": 3, "Carol": 50}
        self.loyalty = {}

    def order_price(self, items):
        return sum(MENU[i]["price"] for i in items)

    def order_ingredients(self, items):
        needed = {}
        for item in items:
            for ing, amount in MENU[item]["ingredients"].items():
                needed[ing] = needed.get(ing, 0) + amount
        return needed
