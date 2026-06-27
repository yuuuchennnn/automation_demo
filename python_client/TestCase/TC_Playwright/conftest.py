"""
Playwright UI test fixtures.

Provides session-scoped browser/page fixture using Playwright's
built-in browser management (no external driver required).

Key advantages over Selenium:
- Auto-downloads browsers (chromium/firefox/webkit)
- Built-in auto-waiting
- No webdriver-manager needed
"""
import pytest
from playwright.sync_api import sync_playwright
from loguru import logger


@pytest.fixture(scope="session")
def playwright_instance():
    """Session-level Playwright instance. Launched once for all tests."""
    logger.info("[Playwright] Starting...")
    with sync_playwright() as pw:
        yield pw
    logger.info("[Playwright] Stopped.")


@pytest.fixture(scope="session")
def browser(playwright_instance, env):
    """
    Session-level Chromium browser (Playwright).

    Uses Playwright's built-in browser management.
    Headless mode for CI compatibility.
    """
    base_url = env["SAUCEDEMO"]["base_url"]

    browser_instance = playwright_instance.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"],
    )
    logger.info("[Playwright] Browser launched — base URL: {}", base_url)
    yield browser_instance
    logger.info("[Playwright] Closing browser...")
    browser_instance.close()


@pytest.fixture(scope="function")
def page(browser, env):
    """
    Function-level page (isolated context per test).

    Playwright's BrowserContext provides:
    - Clean cookies/localStorage per test
    - Parallel test isolation
    """
    base_url = env["SAUCEDEMO"]["base_url"]

    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        base_url=base_url,
    )

    page_instance = context.new_page()
    page_instance.base_url = base_url

    logger.info("[Playwright] New page created")
    yield page_instance

    logger.info("[Playwright] Closing page context...")
    context.close()
