"""
SauceDemo Products / Inventory Page Object.

URL: /inventory.html
"""
from selenium.webdriver.common.by import By
from pages.selenium.base_page import BasePage


class ProductsPage(BasePage):
    """Page Object for SauceDemo products/inventory page."""

    # --- Locators ---
    PAGE_TITLE = (By.CLASS_NAME, "title")
    PRODUCT_ITEMS = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAME = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_DESC = (By.CLASS_NAME, "inventory_item_desc")
    PRODUCT_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_PREFIX = "add-to-cart"
    REMOVE_PREFIX = "remove"
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")

    # --- Page URL ---
    PATH = "/inventory.html"

    def is_loaded(self) -> bool:
        """Verify the products page has loaded."""
        try:
            title = self.get_text(*self.PAGE_TITLE)
            return title == "Products"
        except Exception:
            return False

    def get_title(self) -> str:
        """Get the page title text."""
        return self.get_text(*self.PAGE_TITLE)

    def get_product_count(self) -> int:
        """Return the number of product items displayed."""
        return len(self.find_all(*self.PRODUCT_ITEMS))

    def get_product_names(self) -> list:
        """Return a list of all product names."""
        names = []
        for item in self.find_all(*self.PRODUCT_ITEMS):
            names.append(item.find_element(*self.PRODUCT_NAME).text)
        return names

    def _product_id_from_name(self, product_name: str) -> str:
        """Convert display name to SauceDemo button ID suffix.
        e.g. 'Sauce Labs Backpack' → 'sauce-labs-backpack'
        """
        return product_name.lower().replace(" ", "-")

    def add_item_to_cart(self, product_name: str):
        """
        Add a product to the shopping cart by its display name.

        Uses SauceDemo's ID pattern: add-to-cart-{kebab-name}
        """
        slug = self._product_id_from_name(product_name)
        btn_id = f"{self.ADD_TO_CART_PREFIX}-{slug}"
        self.click(By.ID, btn_id)
        return self

    def get_cart_count(self) -> str:
        """Get the shopping cart badge count."""
        try:
            return self.get_text(*self.SHOPPING_CART_BADGE)
        except Exception:
            return "0"

    def go_to_cart(self):
        """Click the shopping cart link and return CartPage."""
        self.click(*self.SHOPPING_CART_LINK)
        from pages.selenium.cart_page import CartPage
        return CartPage(self.driver)

    def sort_by(self, option_value: str):
        """Select a sort option. e.g. 'lohi', 'hilo', 'az', 'za'."""
        from selenium.webdriver.support.ui import Select
        dropdown = self.find(*self.SORT_DROPDOWN)
        Select(dropdown).select_by_value(option_value)
        return self
