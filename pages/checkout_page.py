from playwright.sync_api import Page

class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name = page.locator("[data-test='firstName']")
        self.last_name = page.locator("[data-test='lastName']")
        self.postal_code = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        self.finish_button = page.locator("[data-test='finish']")
        self.error_message = page.locator("[data-test='error']")
        self.success_header = page.locator("[data-test='complete-header']")
        self.cancel_button = page.locator("[data-test='cancel']")

    def fill_details(self, first: str, last: str, postal: str):
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal)

    def continue_checkout(self):
        self.continue_button.click()

    def finish(self):
        self.finish_button.click()

    def get_error(self):
        return self.error_message.text_content()

    def is_order_complete(self):
        return self.success_header.is_visible()

    def cancel(self):
        self.cancel_button.click()
