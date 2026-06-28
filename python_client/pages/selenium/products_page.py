"""
SauceDemo Products / Inventory Page Object (Selenium).

URL: /inventory.html
"""
from selenium.webdriver.common.by import By
from pages.selenium.base_page import BasePage


class ProductsPage(BasePage):
    """Page Object for SauceDemo products/inventory page."""

    PAGE_TITLE = (By.CLASS_NAME, "title")
    PRODUCT_ITEMS = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAME = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICE = (By.CLASS_NAME, "inventory_item_price")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")

    PATH = "/inventory.html"

    def is_loaded(self) -> bool:
        try:
            return self.get_text(*self.PAGE_TITLE) == "Products"
        except Exception:
            return False

    def get_title(self) -> str:
        return self.get_text(*self.PAGE_TITLE)

    def get_product_count(self) -> int:
        return len(self.find_all(*self.PRODUCT_ITEMS))

    def get_product_names(self) -> list:
        return [item.find_element(*self.PRODUCT_NAME).text
                for item in self.find_all(*self.PRODUCT_ITEMS)]

    def add_item_to_cart(self, product_name: str):
        """Add a product to cart by display name. Uses data-test attribute."""
        slug = product_name.lower().replace(" ", "-")
        self.click(By.CSS_SELECTOR, f"[data-test='add-to-cart-{slug}']")
        return self

    def get_cart_count(self) -> str:
        """
        Get cart badge count. Uses find_elements (instant, zero-wait)
        because the badge element only exists when items are in the cart.
        """
        els = self.driver.find_elements(*self.SHOPPING_CART_BADGE)
        return els[0].text if els else "0"

    def go_to_cart(self):
        self.click(*self.SHOPPING_CART_LINK)
        from pages.selenium.cart_page import CartPage
        return CartPage(self.driver)

    def sort_by(self, option_value: str):
        from selenium.webdriver.support.ui import Select
        Select(self.find(*self.SORT_DROPDOWN)).select_by_value(option_value)
        return self
