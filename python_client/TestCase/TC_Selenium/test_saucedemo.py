"""
SauceDemo Selenium POM Test Cases.

Covers:
- Complete E2E checkout flow (happy path)
- Login failure scenario (locked user)

Uses the Page Object Model pattern with data-driven YAML test data.
"""
import pytest
from loguru import logger

from pages.selenium.login_page import LoginPage
from pages.selenium.overview_page import CheckoutCompletePage
from utils.data_reader import yamlDataProvider


class TestSauceDemo:

    @pytest.mark.ui_selenium
    @pytest.mark.parametrize("testdata", yamlDataProvider("TestData/Selenium/saucedemo_checkout.yaml"))
    def test_saucedemo(self, browser, testdata):
        """
        SauceDemo E2E test — dispatches based on testId.
        """
        test_id = testdata.get("caseid", "")

        if "tc-sauce-1" in test_id:
            self._test_complete_checkout(browser, testdata)
        elif "tc-sauce-2" in test_id:
            self._test_login_failure(browser, testdata)
        else:
            pytest.skip(f"Unknown testId: {test_id}")

    # ------------------------------------------------------------------
    #  Happy Path: complete checkout flow
    # ------------------------------------------------------------------
    def _test_complete_checkout(self, browser, testdata):
        logger.info("=== TC-SAUCE-1: Complete checkout flow ===")

        username = testdata["username"]
        password = testdata["password"]
        first_name = testdata["checkout_info"]["first_name"]
        last_name = testdata["checkout_info"]["last_name"]
        postal_code = testdata["checkout_info"]["postal_code"]
        expected_products = testdata["expected_products"]
        expected_header = testdata["expected_complete_header"]

        # 1. Open login page
        login_page = LoginPage(browser).open()
        assert login_page.is_login_page(), "Login page did not load"
        logger.info("[OK] Login page loaded")

        # 2. Login
        products_page = login_page.login(username, password)

        # 3. Verify we're on the products page
        assert products_page.is_loaded(), "Products page did not load"
        assert products_page.get_title() == "Products"
        logger.info("[OK] Products page loaded — title: {}", products_page.get_title())

        # 4. Add two products to cart
        for product in expected_products:
            products_page.add_item_to_cart(product)
            logger.info("[OK] Added to cart: {}", product)

        # 5. Verify cart badge count
        assert products_page.get_cart_count() == str(len(expected_products)), \
            f"Cart badge expected {len(expected_products)} but got {products_page.get_cart_count()}"
        logger.info("[OK] Cart badge shows: {}", products_page.get_cart_count())

        # 6. Go to cart
        cart_page = products_page.go_to_cart()

        # 7. Verify items in cart
        assert cart_page.get_item_count() == len(expected_products)
        cart_names = cart_page.get_item_names()
        for product in expected_products:
            assert product in cart_names, f"'{product}' not found in cart: {cart_names}"
        logger.info("[OK] Cart contains {} items: {}", cart_page.get_item_count(), cart_names)

        # 8. Checkout
        checkout_page = cart_page.checkout()
        assert checkout_page.is_loaded(), "Checkout page did not load"

        # 9. Fill shipping info
        checkout_page.fill_checkout_info(first_name, last_name, postal_code)
        logger.info("[OK] Shipping info filled: {} {} / {}", first_name, last_name, postal_code)

        # 10. Continue to overview
        overview_page = checkout_page.continue_checkout()
        assert overview_page.is_loaded(), "Overview page did not load"

        # 11. Verify overview
        assert overview_page.get_item_count() == len(expected_products)
        total = overview_page.get_total()
        assert total, "Total should not be empty"
        logger.info("[OK] Overview: {} items, total: {}", overview_page.get_item_count(), total)

        # 12. Finish
        overview_page.finish()

        # 13. Verify completion
        complete_page = CheckoutCompletePage(browser)
        assert complete_page.get_complete_header() == expected_header, \
            f"Expected '{expected_header}' but got '{complete_page.get_complete_header()}'"
        logger.info("[OK] Order complete — header: {}", complete_page.get_complete_header())
        logger.info("[OK] Complete text: {}", complete_page.get_complete_text())

        logger.info("=== TC-SAUCE-1: PASSED ===")

    # ------------------------------------------------------------------
    #  Negative: locked out user login
    # ------------------------------------------------------------------
    def _test_login_failure(self, browser, testdata):
        logger.info("=== TC-SAUCE-2: Login failure — locked out user ===")

        username = testdata["username"]
        password = testdata["password"]
        expected_error = testdata["expected_error"]

        # 1. Open login page
        login_page = LoginPage(browser).open()
        assert login_page.is_login_page(), "Login page did not load"

        # 2. Attempt login
        login_page.enter_username(username)
        login_page.enter_password(password)
        login_page.click(*LoginPage.LOGIN_BUTTON)

        # 3. Verify error message
        actual_error = login_page.get_error_message()
        assert actual_error == expected_error, \
            f"Expected error '{expected_error}' but got '{actual_error}'"
        logger.info("[OK] Error message displayed: {}", actual_error)

        logger.info("=== TC-SAUCE-2: PASSED ===")
