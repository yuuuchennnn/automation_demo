"""
SauceDemo Cart Page Object (Playwright).

URL: /cart.html
"""
from pages.playwright.base_page import BasePage


class CartPage(BasePage):
    """Page Object for SauceDemo shopping cart page."""

    CART_ITEMS = ".cart_item"
    ITEM_NAME = ".inventory_item_name"
    CHECKOUT_BTN = "#checkout"

    PATH = "/cart.html"

    def is_loaded(self) -> bool:
        return self.locator(self.CHECKOUT_BTN).is_visible()

    def get_item_count(self) -> int:
        # locator.count() is instant — page should be loaded by now via checkout() navigation
        return self.locator(self.CART_ITEMS).count()

    def get_item_names(self) -> list:
        return self.locator(self.ITEM_NAME).all_text_contents()

    def remove_item(self, product_name: str):
        slug = product_name.lower().replace(" ", "-")
        self.click(f"[data-test='remove-{slug}']")
        return self

    def checkout(self):
        self.click(self.CHECKOUT_BTN)
        from pages.playwright.checkout_page import CheckoutPage
        return CheckoutPage(self.page)
