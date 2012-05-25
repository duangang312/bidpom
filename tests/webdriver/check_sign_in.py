#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from selenium.webdriver.support.ui import WebDriverWait


@pytest.mark.nondestructive
class TestSignIn:

    def test_sign_in_helper(self, mozwebqa):
        from ... import BrowserID
        browser_id = BrowserID(mozwebqa.selenium, mozwebqa.timeout)
        browser_id.sign_in(mozwebqa.email, mozwebqa.password)

        WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
            lambda s: s.find_element_by_id('loggedin').is_displayed())

    def test_sign_in(self, mozwebqa):
        from ...pages.webdriver.sign_in import SignIn
        signin = SignIn(mozwebqa.selenium, mozwebqa.timeout)
        signin.email = mozwebqa.email
        signin.click_next()
        signin.password = mozwebqa.password
        signin.click_sign_in()

        signin.switch_to_main_window()

        WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
            lambda s: s.find_element_by_id('loggedin').is_displayed())

    def test_sign_in_new_user_helper(self, mozwebqa):
        unregistered_email_address = '%s@restmail.net' % time.time()

        from ... import BrowserID
        browser_id = BrowserID(mozwebqa.selenium, mozwebqa.timeout)
        browser_id.sign_in_new_user(unregistered_email_address)

        WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
            lambda s: s.find_element_by_id('loggedout').is_displayed())

    def test_sign_in_new_user(self, mozwebqa):
        unregistered_email_address = '%s@restmail.net' % time.time()

        from ...pages.webdriver.sign_in import SignIn
        signin = SignIn(mozwebqa.selenium, mozwebqa.timeout)
        signin.email= unregistered_email_address
        signin.click_next()
        signin.click_verify_email()
        signin.close_persona_window()
        signin.switch_to_main_window()

        WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
            lambda s: s.find_element_by_id('loggedout').is_displayed())
