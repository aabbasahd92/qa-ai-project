from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator("[data-test='username']")
        self.password = page.locator("[data-test='password']")
        self.login_button = page.locator("[data-test='login-button']")
        self.error_message = page.locator("[data-test='error']")

    def goto(self):
        self.page.goto("https://www.saucedemo.com")

    def login(self, username: str, password: str):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()

    def get_error(self):
        return self.error_message.text_content()

    def is_logged_in(self):
        return "/inventory" in self.page.url
