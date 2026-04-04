from playwright.sync_api import Page, expect

class ProductsPage:
    def __init__(self, page: Page):
        self.page = page
        self.sort_dropdown = page.locator("[data-test='product-sort-container']")
        self.product_names = page.locator("[data-test='inventory-item-name']")
        self.product_prices = page.locator("[data-test='inventory-item-price']")
        self.product_items = page.locator("[data-test='inventory-item']")
        self.cart_icon = page.locator(".shopping_cart_link")
        self.cart_badge = page.locator("[data-test='shopping-cart-badge']")

    def goto(self):
        self.page.goto("https://www.saucedemo.com")
        self.page.fill("[data-test='username']", "standard_user")
        self.page.fill("[data-test='password']", "secret_sauce")
        self.page.click("[data-test='login-button']")

    def sort_by(self, option: str):
        self.sort_dropdown.select_option(option)

    def get_product_names(self):
        return self.product_names.all_text_contents()

    def get_product_prices(self):
        prices = self.product_prices.all_text_contents()
        return [float(p.replace("$", "")) for p in prices]

    def get_product_count(self):
        return self.product_items.count()

    def add_product_to_cart(self, index: int):
        buttons = self.page.locator("[data-test^='add-to-cart']")
        buttons.nth(index).click()

    def get_cart_count(self):
        if self.cart_badge.is_visible():
            return int(self.cart_badge.text_content())
        return 0
