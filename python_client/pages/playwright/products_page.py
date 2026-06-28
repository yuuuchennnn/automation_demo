"""
SauceDemo Products / Inventory Page Object (Playwright).

URL: /inventory.html
"""
from pages.playwright.base_page import BasePage


class ProductsPage(BasePage):
    """Page Object for SauceDemo products/inventory page."""

    TITLE = ".title"
    PRODUCT_ITEMS = ".inventory_item"
    PRODUCT_NAME = ".inventory_item_name"
    PRODUCT_PRICE = ".inventory_item_price"
    SHOPPING_CART_LINK = ".shopping_cart_link"
    SHOPPING_CART_BADGE = ".shopping_cart_badge"
    SORT_DROPDOWN = ".product_sort_container"

    PATH = "/inventory.html"

    def is_loaded(self) -> bool:
        return self.get_text(self.TITLE) == "Products"

    def get_title(self) -> str:
        return self.get_text(self.TITLE)

    def get_product_count(self) -> int:
        return self.locator(self.PRODUCT_ITEMS).count()

    def get_product_names(self) -> list:
        return self.locator(self.PRODUCT_NAME).all_text_contents()

    def add_item_to_cart(self, product_name: str):
        """Add a product to cart by display name. Uses data-test attribute."""
        slug = product_name.lower().replace(" ", "-")
        self.click(f"[data-test='add-to-cart-{slug}']")
        return self

    def get_cart_count(self) -> str:
        """
        Get cart badge count. Waits briefly for the badge to appear
        after an add-to-cart click (DOM update is async).
        """
        try:
            self.locator(self.SHOPPING_CART_BADGE).wait_for(
                state="attached", timeout=5000
            )
            return self.get_text(self.SHOPPING_CART_BADGE)
        except Exception:
            return "0"

    def go_to_cart(self):
        self.click(self.SHOPPING_CART_LINK)
        from pages.playwright.cart_page import CartPage
        return CartPage(self.page)

    def sort_by(self, option_value: str):
        self.locator(self.SORT_DROPDOWN).select_option(value=option_value)
        return self
