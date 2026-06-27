"""
Selenium UI test fixtures.

Provides session-scoped browser fixture with webdriver-manager
for automatic ChromeDriver version resolution.
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger


@pytest.fixture(scope="session")
def browser(env):
    """
    Session-level Chrome browser instance (Selenium).

    - webdriver-manager auto-installs matching ChromeDriver
    - Headless mode for CI compatibility
    - Session scope: one browser shared by all Selenium tests
    """
    base_url = env["SAUCEDEMO"]["base_url"]

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    logger.info("Starting Chrome browser (Selenium, headless)...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    driver.base_url = base_url

    logger.info("[Selenium] Browser ready — base URL: {}", base_url)

    yield driver

    logger.info("[Selenium] Quitting browser...")
    driver.quit()
