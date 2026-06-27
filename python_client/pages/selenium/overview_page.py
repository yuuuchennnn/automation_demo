"""
SauceDemo Overview Page Object (Step Two: order summary).

URL: /checkout-step-two.html
"""
from selenium.webdriver.common.by import By
from pages.selenium.base_page import BasePage


class OverviewPage(BasePage):
    """Page Object for checkout step two — order overview / summary."""

    # --- Locators ---
    OVERVIEW_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    SUMMARY_TOTAL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")
    CANCEL_BUTTON = (By.ID, "cancel")

    # --- Page URL ---
    PATH = "/checkout-step-two.html"

    def is_loaded(self) -> bool:
        """Verify overview page loaded."""
        try:
            self.find(*self.FINISH_BUTTON)
            return True
        except Exception:
            return False

    def get_item_count(self) -> int:
        """Return number of items in the order overview."""
        return len(self.find_all(*self.OVERVIEW_ITEMS))

    def get_item_names(self) -> list:
        """Return list of product names in the overview."""
        names = []
        for item in self.find_all(*self.OVERVIEW_ITEMS):
            names.append(item.find_element(*self.ITEM_NAME).text)
        return names

    def get_total(self) -> str:
        """Get the total price label text."""
        return self.get_text(*self.SUMMARY_TOTAL)

    def finish(self):
        """Click finish — returns None (redirects to checkout-complete)."""
        self.click(*self.FINISH_BUTTON)


class CheckoutCompletePage(BasePage):
    """Page Object for checkout complete / confirmation page.

    URL: /checkout-complete.html
    """

    # --- Locators ---
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    # --- Page URL ---
    PATH = "/checkout-complete.html"

    def get_complete_header(self) -> str:
        """Get the completion header text (e.g. 'Thank you for your order!')."""
        return self.get_text(*self.COMPLETE_HEADER)

    def get_complete_text(self) -> str:
        """Get the completion message text."""
        return self.get_text(*self.COMPLETE_TEXT)

    def back_to_products(self):
        """Click 'Back Home' to return to products page."""
        self.click(*self.BACK_HOME_BUTTON)
        from pages.selenium.products_page import ProductsPage
        return ProductsPage(self.driver)
