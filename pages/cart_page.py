from playwright.sync_api import Page

class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.cart_items = page.locator("[data-test='inventory-item']")
        self.checkout_button = page.locator("[data-test='checkout']")
        self.continue_shopping = page.locator("[data-test='continue-shopping']")
        self.remove_buttons = page.locator("[data-test^='remove']")

    def goto(self):
        self.page.goto("https://www.saucedemo.com/cart.html")

    def get_item_count(self):
        return self.cart_items.count()

    def checkout(self):
        self.checkout_button.click()

    def remove_item(self, index: int):
        self.remove_buttons.nth(index).click()
