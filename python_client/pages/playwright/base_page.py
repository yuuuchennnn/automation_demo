"""
Playwright Page Object Model - BasePage

Playwright has built-in auto-waiting for most actions (click, fill),
so we don't need explicit WebDriverWait. The BasePage wraps common
locator operations for consistency and convenience.
"""
from playwright.sync_api import Page


class BasePage:
    """Base class for all Playwright Page Objects.

    Args:
        page: Playwright Page instance from the browser fixture.
    """

    DEFAULT_TIMEOUT = 10_000  # ms

    def __init__(self, page: Page):
        self.page = page

    def locator(self, selector: str):
        """Return a Playwright Locator for the given CSS/XPath selector."""
        return self.page.locator(selector)

    def find(self, selector: str):
        """Wait for element to be visible and return the locator."""
        loc = self.locator(selector)
        loc.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        return loc

    def find_all(self, selector: str):
        """Return all matching elements as a Locator (count > 0 assertion)."""
        loc = self.locator(selector)
        loc.first.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        return loc

    def click(self, selector: str):
        """Click an element (Playwright auto-waits for actionability)."""
        self.locator(selector).click(timeout=self.DEFAULT_TIMEOUT)
        return self

    def fill(self, selector: str, text: str):
        """Fill an input field (auto-clears by default)."""
        self.locator(selector).fill(text, timeout=self.DEFAULT_TIMEOUT)
        return self

    def get_text(self, selector: str) -> str:
        """Get the visible text content of an element."""
        return self.locator(selector).text_content(timeout=self.DEFAULT_TIMEOUT) or ""

    def get_input_value(self, selector: str) -> str:
        """Get the current value of an input field."""
        return self.locator(selector).input_value(timeout=self.DEFAULT_TIMEOUT) or ""

    def navigate(self, url: str):
        """Navigate to a URL."""
        self.page.goto(url, timeout=self.DEFAULT_TIMEOUT)
        return self

    def get_current_url(self) -> str:
        return self.page.url

    def wait_for_url(self, substring: str):
        """Wait until URL contains the given string."""
        self.page.wait_for_url(f"**{substring}**", timeout=self.DEFAULT_TIMEOUT)
        return self
