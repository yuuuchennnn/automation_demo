"""
Selenium UI test fixtures.

Provides session-scoped browser fixture with webdriver-manager
to auto-resolve the matching ChromeDriver version.

Pytest auto-discovers this conftest from TestCase/TC_Selenium/.
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger


@pytest.fixture(scope="session")
def browser(env):
    """
    Session-level Chrome browser instance.

    - Uses webdriver-manager to auto-install and match ChromeDriver.
    - Runs in headless mode (CI-friendly).
    - Session scope: all UI tests share one browser instance.
    """
    base_url = env["SAUCEDEMO"]["base_url"]

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    logger.info("Starting Chrome browser (headless)...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)

    # Attach base_url for Page Objects
    driver.base_url = base_url

    logger.info("Browser started. Base URL: {}", base_url)

    yield driver

    logger.info("Quitting browser...")
    driver.quit()
