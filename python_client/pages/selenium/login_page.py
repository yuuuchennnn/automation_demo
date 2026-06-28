"""
SauceDemo Login Page Object (Selenium).

URL: https://www.saucedemo.com
"""
from selenium.webdriver.common.by import By
from pages.selenium.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for SauceDemo login page."""

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    PATH = "/"

    def open(self):
        """Navigate to the login page."""
        self.driver.get(self.driver.base_url + self.PATH)
        return self

    def enter_username(self, username: str):
        self.fill(*self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str):
        self.fill(*self.PASSWORD_INPUT, password)
        return self

    def login(self, username: str, password: str):
        self.enter_username(username)
        self.enter_password(password)
        self.click(*self.LOGIN_BUTTON)
        self.wait_for_url_contains("inventory")
        from pages.selenium.products_page import ProductsPage
        return ProductsPage(self.driver)

    def get_error_message(self) -> str:
        return self.get_text(*self.ERROR_MESSAGE)

    def is_login_page(self) -> bool:
        try:
            self.find(*self.LOGIN_BUTTON)
            return True
        except Exception:
            return False
