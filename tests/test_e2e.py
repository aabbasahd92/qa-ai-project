
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

def test_valid_login(login):
    login.login("standard_user", "secret_sauce")
    assert login.is_logged_in()

def test_invalid_login(login):
    login.login("wrong_user", "wrong_pass")
    assert "Epic sadface" in login.get_error()

def test_locked_user_login(login):
    login.login("locked_out_user", "secret_sauce")
    assert "locked out" in login.get_error()

def test_empty_username(login):
    login.login("", "secret_sauce")
    assert "Username is required" in login.get_error()

def test_empty_password(login):
    login.login("standard_user", "")
    assert "Password is required" in login.get_error()

def test_full_e2e_checkout(logged_in):
    products = ProductsPage(logged_in)
    products.add_product_to_cart(0)
    products.add_product_to_cart(1)
    products.cart_icon.click()
    cart = CartPage(logged_in)
    assert cart.get_item_count() == 2
    cart.checkout()
    checkout = CheckoutPage(logged_in)
    checkout.fill_details("Ahmed", "Abbas", "12345")
    checkout.continue_checkout()
    checkout.finish()
    assert checkout.is_order_complete()

def test_checkout_missing_firstname(logged_in):
    products = ProductsPage(logged_in)
    products.add_product_to_cart(0)
    products.cart_icon.click()
    cart = CartPage(logged_in)
    cart.checkout()
    checkout = CheckoutPage(logged_in)
    checkout.fill_details("", "Abbas", "12345")
    checkout.continue_checkout()
    assert "First Name is required" in checkout.get_error()

def test_checkout_missing_lastname(logged_in):
    products = ProductsPage(logged_in)
    products.add_product_to_cart(0)
    products.cart_icon.click()
    cart = CartPage(logged_in)
    cart.checkout()
    checkout = CheckoutPage(logged_in)
    checkout.fill_details("Ahmed", "", "12345")
    checkout.continue_checkout()
    assert "Last Name is required" in checkout.get_error()

def test_checkout_missing_postal(logged_in):
    products = ProductsPage(logged_in)
    products.add_product_to_cart(0)
    products.cart_icon.click()
    cart = CartPage(logged_in)
    cart.checkout()
    checkout = CheckoutPage(logged_in)
    checkout.fill_details("Ahmed", "Abbas", "")
    checkout.continue_checkout()
    assert "Postal Code is required" in checkout.get_error()

def test_remove_item_from_cart(logged_in):
    products = ProductsPage(logged_in)
    products.add_product_to_cart(0)
    products.add_product_to_cart(1)
    products.cart_icon.click()
    cart = CartPage(logged_in)
    assert cart.get_item_count() == 2
    cart.remove_item(0)
    assert cart.get_item_count() == 1

def test_cancel_checkout(logged_in):
    products = ProductsPage(logged_in)
    products.add_product_to_cart(0)
    products.cart_icon.click()
    cart = CartPage(logged_in)
    cart.checkout()
    checkout = CheckoutPage(logged_in)
    checkout.cancel()
    assert "/cart" in logged_in.url

def test_checkout_empty_cart(logged_in):
    cart = CartPage(logged_in)
    cart.goto()
    assert cart.get_item_count() == 0
