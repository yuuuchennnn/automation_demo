"""
SauceDemo Login Page Object (Playwright).

URL: https://www.saucedemo.com
"""
from pages.playwright.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for SauceDemo login page."""

    # CSS selectors
    USERNAME = "#user-name"
    PASSWORD = "#password"
    LOGIN_BTN = "#login-button"
    ERROR_MSG = "[data-test='error']"

    PATH = "/"

    def open(self):
        """Navigate to the login page."""
        self.page.goto(self.page.base_url + self.PATH)
        return self

    def enter_username(self, username: str):
        self.fill(self.USERNAME, username)
        return self

    def enter_password(self, password: str):
        self.fill(self.PASSWORD, password)
        return self

    def login(self, username: str, password: str):
        self.enter_username(username)
        self.enter_password(password)
        self.click(self.LOGIN_BTN)
        self.wait_for_url("inventory")
        from pages.playwright.products_page import ProductsPage
        return ProductsPage(self.page)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MSG)

    def is_login_page(self) -> bool:
        return self.locator(self.LOGIN_BTN).is_visible()
