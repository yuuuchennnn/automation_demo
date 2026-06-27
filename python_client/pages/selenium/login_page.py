"""
SauceDemo Login Page Object.

URL: https://www.saucedemo.com
"""
from selenium.webdriver.common.by import By
from pages.selenium.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for SauceDemo login page."""

    # --- Locators ---
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    # --- Page URL ---
    PATH = "/"

    def open(self):
        """Navigate to the login page."""
        self.driver.get(self.driver.base_url + self.PATH)
        return self

    def enter_username(self, username: str):
        """Fill username field."""
        self.fill(*self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str):
        """Fill password field."""
        self.fill(*self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        """Click the login button and return the next expected page."""
        self.click(*self.LOGIN_BUTTON)
        from pages.selenium.products_page import ProductsPage
        return ProductsPage(self.driver)

    def login(self, username: str, password: str):
        """Perform full login flow."""
        self.enter_username(username)
        self.enter_password(password)
        return self.click_login()

    def get_error_message(self) -> str:
        """Get the error message text (if displayed)."""
        return self.get_text(*self.ERROR_MESSAGE)

    def is_login_page(self) -> bool:
        """Verify we are on the login page."""
        try:
            self.find(*self.LOGIN_BUTTON)
            return True
        except Exception:
            return False
