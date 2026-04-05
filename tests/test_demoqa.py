import pytest
from playwright.sync_api import Page, expect
from pages.demoqa_page import DemoQAPage

def test_simple_alert(page: Page):
    demoqa = DemoQAPage(page)
    demoqa.goto_alerts()
    page.on("dialog", lambda dialog: dialog.accept())
    page.locator("#alertButton").click()

def test_alert_with_text(page: Page):
    demoqa = DemoQAPage(page)
    demoqa.goto_alerts()
    messages = []
    page.on("dialog", lambda dialog: (messages.append(dialog.message), dialog.accept()))
    page.locator("#timerAlertButton").click()
    page.wait_for_timeout(6000)
    assert len(messages) > 0

def test_confirm_alert_accept(page: Page):
    demoqa = DemoQAPage(page)
    demoqa.goto_alerts()
    page.on("dialog", lambda dialog: dialog.accept())
    page.locator("#confirmButton").click()
    result = page.locator("#confirmResult")
    expect(result).to_have_text("You selected Ok")

def test_confirm_alert_dismiss(page: Page):
    demoqa = DemoQAPage(page)
    demoqa.goto_alerts()
    page.on("dialog", lambda dialog: dialog.dismiss())
    page.locator("#confirmButton").click()
    result = page.locator("#confirmResult")
    expect(result).to_have_text("You selected Cancel")

def test_prompt_alert(page: Page):
    demoqa = DemoQAPage(page)
    demoqa.goto_alerts()
    page.on("dialog", lambda dialog: dialog.accept("Ahmed"))
    page.locator("#promtButton").click()
    result = page.locator("#promptResult")
    expect(result).to_have_text("You entered Ahmed")
    
def test_drag_and_drop(page: Page):
    page.set_viewport_size({"width": 1280, "height": 720})
    demoqa = DemoQAPage(page)
    demoqa.goto_droppable()
    page.wait_for_load_state("networkidle")
    source = page.locator("#draggable")
    target = page.locator("#droppable").first
    source.scroll_into_view_if_needed()
    page.wait_for_timeout(1000)
    source_box = source.bounding_box()
    target_box = target.bounding_box()
    print(f"Source: {source_box}")
    print(f"Target: {target_box}")
    page.mouse.move(source_box["x"] + source_box["width"] / 2,
                    source_box["y"] + source_box["height"] / 2)
    page.mouse.down()
    page.wait_for_timeout(500)
    page.mouse.move(target_box["x"] + target_box["width"] / 2,
                    target_box["y"] + target_box["height"] / 2, steps=20)
    page.wait_for_timeout(500)
    page.mouse.up()
    page.wait_for_timeout(1000)
    print(f"Target text: {target.text_content()}")
    expect(target).to_have_text("Dropped!")

def test_slider(page: Page):
    demoqa = DemoQAPage(page)
    demoqa.goto_slider()
    slider = page.locator(".range-slider")
    slider.click()
    page.keyboard.press("ArrowRight")
    page.keyboard.press("ArrowRight")
    page.keyboard.press("ArrowRight")
    value = page.locator("#sliderValue").get_attribute("value")
    assert value is not None

def test_progress_bar_start_stop(page: Page):
    demoqa = DemoQAPage(page)
    demoqa.goto_progress_bar()
    page.locator("#startStopButton").click()
    page.wait_for_timeout(2000)
    page.locator("#startStopButton").click()
    progress = page.locator(".progress-bar")
    style = progress.get_attribute("style")
    assert style is not None
    assert "width" in style

def test_tooltip_hover(page: Page):
    demoqa = DemoQAPage(page)
    demoqa.goto_tooltip()
    button = page.locator("#toolTipButton")
    button.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    button.hover()
    page.wait_for_timeout(2000)
    tooltip = page.locator("[role=tooltip]")
    expect(tooltip).to_be_visible()

def test_datepicker(page: Page):
    demoqa = DemoQAPage(page)
    demoqa.goto_datepicker()
    date_input = page.locator("#datePickerMonthYearInput")
    date_input.fill("04/05/2026")
    date_input.press("Enter")
    value = date_input.input_value()
    assert "2026" in value