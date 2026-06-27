"""
SauceDemo E2E Test Cases — Selenium POM.

Covers:
- Complete checkout flow (happy path)
- Login failure (locked user)
"""
import pytest
from loguru import logger

from pages.selenium.login_page import LoginPage
from pages.selenium.overview_page import CheckoutCompletePage
from utils.data_reader import yamlDataProvider


class TestSauceDemoSelenium:

    @pytest.mark.ui_selenium
    @pytest.mark.parametrize("testdata", yamlDataProvider("TestData/Selenium/saucedemo_checkout.yaml"))
    def test_saucedemo(self, browser, testdata):
        """Dispatch to sub-tests based on testId."""
        test_id = testdata.get("caseid", "")
        if "tc-sauce-1" in test_id:
            self._test_complete_checkout(browser, testdata)
        elif "tc-sauce-2" in test_id:
            self._test_login_failure(browser, testdata)
        else:
            pytest.skip(f"Unknown testId: {test_id}")

    def _test_complete_checkout(self, browser, testdata):
        logger.info("=== [Selenium] TC-SAUCE-1: Complete checkout ===")
        td = testdata
        expected = td["expected_products"]

        # 1. Login
        login_page = LoginPage(browser).open()
        assert login_page.is_login_page()
        products_page = login_page.login(td["username"], td["password"])

        # 2. Products page
        assert products_page.is_loaded()
        assert products_page.get_title() == "Products"
        logger.info("[OK] Products page loaded")

        # 3. Add items
        for name in expected:
            products_page.add_item_to_cart(name)
            logger.info("[OK] Added: {}", name)
        assert products_page.get_cart_count() == str(len(expected))

        # 4. Cart
        cart_page = products_page.go_to_cart()
        assert cart_page.get_item_count() == len(expected)
        for name in expected:
            assert name in cart_page.get_item_names()
        logger.info("[OK] Cart verified — {} items", cart_page.get_item_count())

        # 5. Checkout
        checkout_page = cart_page.checkout()
        assert checkout_page.is_loaded()
        ci = td["checkout_info"]
        checkout_page.fill_checkout_info(ci["first_name"], ci["last_name"], ci["postal_code"])

        # 6. Overview
        overview_page = checkout_page.continue_checkout()
        assert overview_page.is_loaded()
        assert overview_page.get_item_count() == len(expected)
        assert overview_page.get_total()
        logger.info("[OK] Overview — total: {}", overview_page.get_total())

        # 7. Finish
        overview_page.finish()
        complete = CheckoutCompletePage(browser)
        assert complete.get_complete_header() == td["expected_complete_header"]
        logger.info("[OK] Complete: {}", complete.get_complete_header())
        logger.info("=== [Selenium] TC-SAUCE-1: PASSED ===")

    def _test_login_failure(self, browser, testdata):
        logger.info("=== [Selenium] TC-SAUCE-2: Login failure ===")
        td = testdata

        login_page = LoginPage(browser).open()
        assert login_page.is_login_page()

        login_page.enter_username(td["username"])
        login_page.enter_password(td["password"])
        login_page.click(*LoginPage.LOGIN_BUTTON)

        assert login_page.get_error_message() == td["expected_error"]
        logger.info("[OK] Error: {}", login_page.get_error_message())
        logger.info("=== [Selenium] TC-SAUCE-2: PASSED ===")
