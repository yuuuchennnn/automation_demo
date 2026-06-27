"""
SauceDemo Checkout Page Object (Playwright) — Step One: shipping info.

URL: /checkout-step-one.html
"""
from pages.playwright.base_page import BasePage


class CheckoutPage(BasePage):
    """Page Object for checkout step one — shipping info form."""

    FIRST_NAME = "#first-name"
    LAST_NAME = "#last-name"
    POSTAL_CODE = "#postal-code"
    CONTINUE_BTN = "#continue"
    ERROR_MSG = "[data-test='error']"

    PATH = "/checkout-step-one.html"

    def is_loaded(self) -> bool:
        return self.locator(self.CONTINUE_BTN).is_visible()

    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str):
        self.fill(self.FIRST_NAME, first_name)
        self.fill(self.LAST_NAME, last_name)
        self.fill(self.POSTAL_CODE, postal_code)
        return self

    def continue_checkout(self):
        self.click(self.CONTINUE_BTN)
        from pages.playwright.overview_page import OverviewPage
        return OverviewPage(self.page)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MSG)
