"""
SauceDemo Checkout Page Object (Step One: shipping information).

URL: /checkout-step-one.html
"""
from selenium.webdriver.common.by import By
from pages.selenium.base_page import BasePage


class CheckoutPage(BasePage):
    """Page Object for checkout step one — shipping info form."""

    # --- Locators ---
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    # --- Page URL ---
    PATH = "/checkout-step-one.html"

    def is_loaded(self) -> bool:
        """Verify checkout step one page loaded."""
        try:
            self.find(*self.CONTINUE_BUTTON)
            return True
        except Exception:
            return False

    def fill_first_name(self, first_name: str):
        """Fill first name field."""
        self.fill(*self.FIRST_NAME_INPUT, first_name)
        return self

    def fill_last_name(self, last_name: str):
        """Fill last name field."""
        self.fill(*self.LAST_NAME_INPUT, last_name)
        return self

    def fill_postal_code(self, postal_code: str):
        """Fill postal code field."""
        self.fill(*self.POSTAL_CODE_INPUT, postal_code)
        return self

    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str):
        """Fill all shipping information fields."""
        self.fill_first_name(first_name)
        self.fill_last_name(last_name)
        self.fill_postal_code(postal_code)
        return self

    def continue_checkout(self):
        """Click continue and return OverviewPage."""
        self.click(*self.CONTINUE_BUTTON)
        from pages.selenium.overview_page import OverviewPage
        return OverviewPage(self.driver)

    def get_error_message(self) -> str:
        """Get error message text if displayed."""
        return self.get_text(*self.ERROR_MESSAGE)
