from playwright.sync_api import Page
from pages.home_page import HomePage

def test_title(home):
    assert home.page.title() == "My Test Site"

def test_search(home):
    home.search("Playwright")
    assert home.get_result() == "You searched: Playwright"

def test_empty_search(home):
    home.search("")
    assert home.get_result() == "You searched: "

def test_special_characters(home):
    home.search("!@#$%")
    assert home.get_result() == "You searched: !@#$%"


def test_parallel_failure(home):
    assert home.page.title() == "Wrong Title"
