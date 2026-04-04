import os
from PIL import Image, ImageChops
from playwright.sync_api import Page
from pages.login_page import LoginPage

BASELINE_DIR = "visual-baselines"
os.makedirs(BASELINE_DIR, exist_ok=True)

def compare_screenshot(page: Page, name: str):
    actual_path = f"{BASELINE_DIR}/{name}-actual.png"
    baseline_path = f"{BASELINE_DIR}/{name}-baseline.png"
    page.screenshot(path=actual_path)
    if not os.path.exists(baseline_path):
        page.screenshot(path=baseline_path)
        print(f"Baseline created: {baseline_path}")
        return
    baseline = Image.open(baseline_path)
    actual = Image.open(actual_path)
    diff = ImageChops.difference(baseline, actual)
    assert diff.getbbox() is None, f"Visual difference detected in {name}"

def test_login_page_visual(page: Page):
    page.goto("https://www.saucedemo.com")
    page.wait_for_load_state("networkidle")
    compare_screenshot(page, "login-page")

def test_inventory_page_visual(page: Page):
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")
    page.wait_for_url("**/inventory.html")
    page.wait_for_load_state("networkidle")
    compare_screenshot(page, "inventory-page")

def test_cart_page_visual(page: Page):
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")
    page.wait_for_url("**/inventory.html")
    page.locator("[data-test^='add-to-cart']").first.click()
    page.locator(".shopping_cart_link").click()
    page.wait_for_load_state("networkidle")
    compare_screenshot(page, "cart-page")