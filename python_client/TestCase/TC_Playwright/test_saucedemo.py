"""
SauceDemo E2E Test Cases — Playwright POM.

Covers the same scenarios as the Selenium version,
demonstrating Playwright's sync API with auto-waiting.
"""
import pytest
from loguru import logger

from pages.playwright.login_page import LoginPage
from pages.playwright.overview_page import CheckoutCompletePage
from utils.data_reader import yamlDataProvider


class TestSauceDemoPlaywright:

    @pytest.mark.ui_playwright
    @pytest.mark.parametrize("testdata", yamlDataProvider("TestData/Playwright/saucedemo_checkout.yaml"))
    def test_saucedemo(self, page, testdata):
        """Dispatch to sub-tests based on testId."""
        test_id = testdata.get("caseid", "")
        if "tc-pw-1" in test_id:
            self._test_complete_checkout(page, testdata)
        elif "tc-pw-2" in test_id:
            self._test_login_failure(page, testdata)
        else:
            pytest.skip(f"Unknown testId: {test_id}")

    def _test_complete_checkout(self, page, testdata):
        logger.info("=== [Playwright] TC-PW-1: Complete checkout ===")
        td = testdata
        expected = td["expected_products"]

        # 1. Login
        login_page = LoginPage(page).open()
        assert login_page.is_login_page()
        products_page = login_page.login(td["username"], td["password"])

        # 2. Products page — Playwright auto-waits for elements
        assert products_page.is_loaded()
        assert products_page.get_title() == "Products"
        logger.info("[OK] Products page loaded")

        # 3. Add items to cart
        for name in expected:
            products_page.add_item_to_cart(name)
            logger.info("[OK] Added: {}", name)
        assert products_page.get_cart_count() == str(len(expected))

        # 4. Cart page
        cart_page = products_page.go_to_cart()
        assert cart_page.get_item_count() == len(expected)
        for name in expected:
            assert name in cart_page.get_item_names()
        logger.info("[OK] Cart verified — {} items", cart_page.get_item_count())

        # 5. Checkout — fill shipping info
        checkout_page = cart_page.checkout()
        assert checkout_page.is_loaded()
        ci = td["checkout_info"]
        checkout_page.fill_checkout_info(ci["first_name"], ci["last_name"], ci["postal_code"])

        # 6. Overview page
        overview_page = checkout_page.continue_checkout()
        assert overview_page.is_loaded()
        assert overview_page.get_item_count() == len(expected)
        assert overview_page.get_total()
        logger.info("[OK] Overview — total: {}", overview_page.get_total())

        # 7. Finish — verify completion
        overview_page.finish()
        complete = CheckoutCompletePage(page)
        assert complete.get_complete_header() == td["expected_complete_header"]
        logger.info("[OK] Complete: {}", complete.get_complete_header())
        logger.info("=== [Playwright] TC-PW-1: PASSED ===")

    def _test_login_failure(self, page, testdata):
        logger.info("=== [Playwright] TC-PW-2: Login failure ===")
        td = testdata

        login_page = LoginPage(page).open()
        assert login_page.is_login_page()

        login_page.enter_username(td["username"])
        login_page.enter_password(td["password"])
        login_page.click(LoginPage.LOGIN_BTN)

        assert login_page.get_error_message() == td["expected_error"]
        logger.info("[OK] Error: {}", login_page.get_error_message())
        logger.info("=== [Playwright] TC-PW-2: PASSED ===")
