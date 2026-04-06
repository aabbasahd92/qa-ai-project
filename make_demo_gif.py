"""
Creates an animated GIF showing the E2E test flow:
  Login → Products → Add to Cart → Checkout
Uses Playwright to capture browser screenshots at each step.
"""

import os
from PIL import Image
from playwright.sync_api import sync_playwright

STEPS = []

def shot(page, label, pause_ms=800):
    """Take a screenshot, resize, and store for GIF."""
    path = f"/tmp/demo_frame_{len(STEPS):02d}.png"
    page.screenshot(path=path)
    img = Image.open(path).convert("RGB")
    img = img.resize((900, 600), Image.LANCZOS)
    # Duplicate frames so the step lingers longer
    frames = pause_ms // 100
    STEPS.extend([img] * max(frames, 1))
    print(f"  [{len(STEPS):3d} frames] {label}")


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 900, "height": 600})
        page = ctx.new_page()

        # ── 1. Login page ──────────────────────────────────────────────
        page.goto("https://www.saucedemo.com")
        page.wait_for_load_state("domcontentloaded")
        shot(page, "Login page loaded", pause_ms=1200)

        page.fill("#user-name", "standard_user")
        shot(page, "Typing username", pause_ms=600)

        page.fill("#password", "secret_sauce")
        shot(page, "Typing password", pause_ms=600)

        page.click("#login-button")
        page.wait_for_url("**/inventory.html")
        shot(page, "Logged in — Products page", pause_ms=1500)

        # ── 2. Sort products ────────────────────────────────────────────
        page.select_option(".product_sort_container", "za")
        shot(page, "Sorted Z→A", pause_ms=1000)

        page.select_option(".product_sort_container", "lohi")
        shot(page, "Sorted price low→high", pause_ms=1000)

        # ── 3. Add items to cart ────────────────────────────────────────
        page.click("text=Add to cart", )
        shot(page, "Item 1 added to cart", pause_ms=800)

        # add second item
        add_buttons = page.locator("button:has-text('Add to cart')")
        if add_buttons.count() > 0:
            add_buttons.first.click()
            shot(page, "Item 2 added to cart", pause_ms=800)

        # ── 4. Cart page ────────────────────────────────────────────────
        page.click(".shopping_cart_link")
        page.wait_for_url("**/cart.html")
        shot(page, "Cart — 2 items", pause_ms=1200)

        # ── 5. Checkout step 1 ──────────────────────────────────────────
        page.click("#checkout")
        page.wait_for_url("**/checkout-step-one.html")
        shot(page, "Checkout — Enter info", pause_ms=800)

        page.fill("#first-name", "Ahmed")
        page.fill("#last-name", "Abbas")
        page.fill("#postal-code", "10001")
        shot(page, "Form filled", pause_ms=600)

        page.click("#continue")
        page.wait_for_url("**/checkout-step-two.html")
        shot(page, "Checkout — Order summary", pause_ms=1200)

        # ── 6. Finish ───────────────────────────────────────────────────
        page.click("#finish")
        page.wait_for_url("**/checkout-complete.html")
        shot(page, "Order complete!", pause_ms=2000)

        browser.close()

    # ── Build GIF ───────────────────────────────────────────────────────
    out = "/Users/ahmedabbas/qa-ai-project/assets/demo.gif"
    first, *rest = STEPS
    first.save(
        out,
        save_all=True,
        append_images=rest,
        duration=100,   # 100 ms per frame
        loop=0,
        optimize=False,
    )
    size_kb = os.path.getsize(out) / 1024
    print(f"\nSaved {out}  ({size_kb:.0f} KB, {len(STEPS)} frames)")


if __name__ == "__main__":
    run()
