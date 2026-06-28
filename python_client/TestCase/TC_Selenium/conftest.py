"""
Selenium UI test fixtures.

Provides session-scoped browser fixture with webdriver-manager
for automatic ChromeDriver version resolution.
"""
import logging
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger

# Suppress Selenium's internal DEBUG-level noise (remote_connection, etc.)
# while keeping project log_cli_level = DEBUG intact.
logging.getLogger("selenium").setLevel(logging.WARNING)


@pytest.fixture(scope="session")
def browser(env):
    """
    Session-level Chrome browser instance (Selenium).

    - webdriver-manager auto-installs matching ChromeDriver
    - Password manager disabled to prevent native "Change your password" popup
    - Session scope: one browser shared by all Selenium tests
    """
    base_url = env["SAUCEDEMO"]["base_url"]

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # ------------------------------------------------------------------
    #  Block Chrome native password-save & change-password dialogs.
    #  These are OS-level prompts — invisible to Selenium — that
    #  silently swallow mouse clicks, causing add-to-cart and other
    #  interactive operations to fail with no error.
    # ------------------------------------------------------------------
    prefs = {
        # core password manager off-switches
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        # the critical one: blocks "Change your password?" bubble
        "profile.password_manager_leak_detection": False,
        # autofill services that trigger password prompts
        "autofill.profile_enabled": False,
        "autofill.credit_card_enabled": False,
    }
    options.add_experimental_option("prefs", prefs)

    logger.info("Starting Chrome browser (Selenium)...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    driver.base_url = base_url

    logger.info("[Selenium] Browser ready — base URL: {}", base_url)

    yield driver

    logger.info("[Selenium] Quitting browser...")
    driver.quit()
