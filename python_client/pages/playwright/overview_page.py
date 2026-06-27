"""
SauceDemo Overview Page Object (Playwright) — Step Two: order summary.

URL: /checkout-step-two.html
Also includes CheckoutCompletePage for /checkout-complete.html
"""
from pages.playwright.base_page import BasePage


class OverviewPage(BasePage):
    """Page Object for checkout step two — order overview."""

    ITEMS = ".cart_item"
    ITEM_NAME = ".inventory_item_name"
    TOTAL = ".summary_total_label"
    FINISH_BTN = "#finish"

    PATH = "/checkout-step-two.html"

    def is_loaded(self) -> bool:
        return self.locator(self.FINISH_BTN).is_visible()

    def get_item_count(self) -> int:
        return self.locator(self.ITEMS).count()

    def get_item_names(self) -> list:
        return self.locator(self.ITEM_NAME).all_text_contents()

    def get_total(self) -> str:
        return self.get_text(self.TOTAL)

    def finish(self):
        self.click(self.FINISH_BTN)


class CheckoutCompletePage(BasePage):
    """Page Object for checkout complete / confirmation page."""

    COMPLETE_HEADER = ".complete-header"
    COMPLETE_TEXT = ".complete-text"
    BACK_HOME_BTN = "#back-to-products"

    PATH = "/checkout-complete.html"

    def is_loaded(self) -> bool:
        return self.locator(self.COMPLETE_HEADER).is_visible()

    def get_complete_header(self) -> str:
        return self.get_text(self.COMPLETE_HEADER)

    def get_complete_text(self) -> str:
        return self.get_text(self.COMPLETE_TEXT)

    def back_to_products(self):
        self.click(self.BACK_HOME_BTN)
        from pages.playwright.products_page import ProductsPage
        return ProductsPage(self.page)
