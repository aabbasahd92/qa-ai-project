
import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.form_page import FormPage
from pages.products_page import ProductsPage
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

@pytest.fixture
def home(page: Page):
    page.goto("http://localhost:8000/index.html", wait_until="load")
    return HomePage(page)

@pytest.fixture
def form(page: Page):
    page.goto("http://localhost:8000/index.html", wait_until="load")
    return FormPage(page)

@pytest.fixture
def products(page: Page):
    products_page = ProductsPage(page)
    products_page.goto()
    return products_page

@pytest.fixture
def login(page: Page):
    login_page = LoginPage(page)
    login_page.goto()
    return login_page

@pytest.fixture
def logged_in(page: Page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("standard_user", "secreHellot_sauce")
    return page

@pytest.fixture
def cart(logged_in):
    return CartPage(logged_in)

@pytest.fixture
def checkout(logged_in):
    return CheckoutPage(logged_in)

