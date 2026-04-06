from playwright.sync_api import Page

class DemoQAPage:
    def __init__(self, page: Page):
        self.page = page

    def goto_alerts(self):
        self.page.goto("https://demoqa.com/alerts")

    def goto_droppable(self):
        self.page.goto("https://demoqa.com/droppable")

    def goto_slider(self):
        self.page.goto("https://demoqa.com/slider")

    def goto_progress_bar(self):
        self.page.goto("https://demoqa.com/progress-bar", timeout=60000)

    def goto_datepicker(self):
        self.page.goto("https://demoqa.com/date-picker")

    def goto_tooltip(self):
        self.page.goto("https://demoqa.com/tool-tips")