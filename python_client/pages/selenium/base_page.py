"""
Selenium Page Object Model - BasePage

Provides common WebDriver operations shared by all Page Objects:
find, click, fill, get_text with explicit waits.
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Base class for all Selenium Page Objects."""

    DEFAULT_TIMEOUT = 10

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    def find(self, by, value):
        """Wait for element presence and return it."""
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def find_all(self, by, value):
        """Wait for at least one element and return all matching elements."""
        self.wait.until(EC.presence_of_element_located((by, value)))
        return self.driver.find_elements(by, value)

    def click(self, by, value):
        """Wait for element to be clickable, then click."""
        self.wait.until(EC.element_to_be_clickable((by, value))).click()

    def fill(self, by, value, text):
        """Clear input field and type text."""
        el = self.find(by, value)
        el.clear()
        el.send_keys(text)

    def get_text(self, by, value):
        """Get visible text of an element."""
        return self.find(by, value).text

    def get_current_url(self):
        """Return the current page URL."""
        return self.driver.current_url

    def wait_for_url_contains(self, partial_url, timeout=None):
        """Wait until URL contains the given string."""
        wait = WebDriverWait(self.driver, timeout or self.DEFAULT_TIMEOUT)
        return wait.until(EC.url_contains(partial_url))
