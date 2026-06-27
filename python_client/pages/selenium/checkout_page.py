"""
SauceDemo Checkout Page Object (Selenium) — Step One: shipping info.

URL: /checkout-step-one.html
"""
from selenium.webdriver.common.by import By
from pages.selenium.base_page import BasePage


class CheckoutPage(BasePage):
    """Page Object for checkout step one — shipping info form."""

    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    PATH = "/checkout-step-one.html"

    def is_loaded(self) -> bool:
        try:
            self.find(*self.CONTINUE_BUTTON)
            return True
        except Exception:
            return False

    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str):
        self.fill(*self.FIRST_NAME_INPUT, first_name)
        self.fill(*self.LAST_NAME_INPUT, last_name)
        self.fill(*self.POSTAL_CODE_INPUT, postal_code)
        return self

    def continue_checkout(self):
        self.click(*self.CONTINUE_BUTTON)
        from pages.selenium.overview_page import OverviewPage
        return OverviewPage(self.driver)

    def get_error_message(self) -> str:
        return self.get_text(*self.ERROR_MESSAGE)
