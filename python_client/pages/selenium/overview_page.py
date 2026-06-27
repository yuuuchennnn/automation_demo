"""
SauceDemo Overview Page Object (Selenium) — Step Two: order summary.

URL: /checkout-step-two.html
Also includes CheckoutCompletePage for /checkout-complete.html
"""
from selenium.webdriver.common.by import By
from pages.selenium.base_page import BasePage


class OverviewPage(BasePage):
    """Page Object for checkout step two — order overview."""

    OVERVIEW_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    SUMMARY_TOTAL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")

    PATH = "/checkout-step-two.html"

    def is_loaded(self) -> bool:
        try:
            self.find(*self.FINISH_BUTTON)
            return True
        except Exception:
            return False

    def get_item_count(self) -> int:
        return len(self.find_all(*self.OVERVIEW_ITEMS))

    def get_item_names(self) -> list:
        return [item.find_element(*self.ITEM_NAME).text
                for item in self.find_all(*self.OVERVIEW_ITEMS)]

    def get_total(self) -> str:
        return self.get_text(*self.SUMMARY_TOTAL)

    def finish(self):
        self.click(*self.FINISH_BUTTON)


class CheckoutCompletePage(BasePage):
    """Page Object for checkout complete / confirmation page."""

    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    PATH = "/checkout-complete.html"

    def is_loaded(self) -> bool:
        try:
            self.find(*self.COMPLETE_HEADER)
            return True
        except Exception:
            return False

    def get_complete_header(self) -> str:
        return self.get_text(*self.COMPLETE_HEADER)

    def get_complete_text(self) -> str:
        return self.get_text(*self.COMPLETE_TEXT)

    def back_to_products(self):
        self.click(*self.BACK_HOME_BUTTON)
        from pages.selenium.products_page import ProductsPage
        return ProductsPage(self.driver)
