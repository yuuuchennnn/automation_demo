"""
SauceDemo Cart Page Object (Selenium).

URL: /cart.html
"""
from selenium.webdriver.common.by import By
from pages.selenium.base_page import BasePage


class CartPage(BasePage):
    """Page Object for SauceDemo shopping cart page."""

    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CART_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    REMOVE_PREFIX = "remove"
    CHECKOUT_BUTTON = (By.ID, "checkout")

    PATH = "/cart.html"

    def is_loaded(self) -> bool:
        try:
            self.find(*self.CHECKOUT_BUTTON)
            return True
        except Exception:
            return False

    def get_item_count(self) -> int:
        return len(self.find_all(*self.CART_ITEMS))

    def get_item_names(self) -> list:
        return [item.find_element(*self.CART_ITEM_NAME).text
                for item in self.find_all(*self.CART_ITEMS)]

    def remove_item(self, product_name: str):
        slug = product_name.lower().replace(" ", "-")
        self.click(By.ID, f"{self.REMOVE_PREFIX}-{slug}")
        return self

    def checkout(self):
        self.click(*self.CHECKOUT_BUTTON)
        from pages.selenium.checkout_page import CheckoutPage
        return CheckoutPage(self.driver)
