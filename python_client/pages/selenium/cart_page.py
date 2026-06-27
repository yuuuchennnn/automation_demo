"""
SauceDemo Cart Page Object.

URL: /cart.html
"""
from selenium.webdriver.common.by import By
from pages.selenium.base_page import BasePage


class CartPage(BasePage):
    """Page Object for SauceDemo shopping cart page."""

    # --- Locators ---
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CART_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    REMOVE_PREFIX = "remove"
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BTN = (By.ID, "continue-shopping")

    # --- Page URL ---
    PATH = "/cart.html"

    def is_loaded(self) -> bool:
        """Verify the cart page loaded."""
        try:
            self.find(*self.CHECKOUT_BUTTON)
            return True
        except Exception:
            return False

    def get_item_count(self) -> int:
        """Return number of items in the cart."""
        return len(self.find_all(*self.CART_ITEMS))

    def get_item_names(self) -> list:
        """Return a list of product names in the cart."""
        names = []
        for item in self.find_all(*self.CART_ITEMS):
            names.append(item.find_element(*self.CART_ITEM_NAME).text)
        return names

    def remove_item(self, product_name: str):
        """Remove an item from the cart by product name."""
        slug = product_name.lower().replace(" ", "-")
        btn_id = f"{self.REMOVE_PREFIX}-{slug}"
        self.click(By.ID, btn_id)
        return self

    def checkout(self):
        """Click checkout and return CheckoutPage."""
        self.click(*self.CHECKOUT_BUTTON)
        from pages.selenium.checkout_page import CheckoutPage
        return CheckoutPage(self.driver)
