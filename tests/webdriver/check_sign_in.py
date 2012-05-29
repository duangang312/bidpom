#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
import uuid

import pytest
from selenium.webdriver.support.ui import WebDriverWait

from ... import BrowserID
from .. import restmail


@pytest.mark.nondestructive
class TestSignIn:

    def test_sign_in_helper(self, mozwebqa):
        browser_id = BrowserID(mozwebqa.selenium, mozwebqa.timeout)
        browser_id.sign_in(mozwebqa.email, mozwebqa.password)

        WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
            lambda s: s.find_element_by_id('loggedin').is_displayed())

    def test_sign_in(self, mozwebqa):
        from ...pages.webdriver.sign_in import SignIn
        signin = SignIn(mozwebqa.selenium, mozwebqa.timeout, expect='new')
        signin.email = mozwebqa.email
        signin.click_next(expect='password')
        signin.password = mozwebqa.password
        signin.click_sign_in()

        WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
            lambda s: s.find_element_by_id('loggedin').is_displayed())

    def test_sign_in_new_user_helper(self, mozwebqa):
        restmail_username = 'bidpom_%s' % uuid.uuid1()
        browser_id = BrowserID(mozwebqa.selenium, mozwebqa.timeout)
        print 'signing in as %s@restmail.net' % restmail_username
        browser_id.sign_in('%s@restmail.net' % restmail_username)
        mail = restmail.get_mail(restmail_username)
        assert 'Thanks for verifying' in mail[0]['text']

    def test_sign_in_new_user(self, mozwebqa):
        restmail_username = 'bidpom_%s' % uuid.uuid1()

        from ...pages.webdriver.sign_in import SignIn
        signin = SignIn(mozwebqa.selenium, mozwebqa.timeout, expect='new')
        print 'signing in as %s@restmail.net' % restmail_username
        signin.email = '%s@restmail.net' % restmail_username
        signin.click_next(expect='verify')
        signin.click_verify_email()
        signin.close_window()
        signin.switch_to_main_window()
        mail = restmail.get_mail(restmail_username)
        assert 'Thanks for verifying' in mail[0]['text']

    def test_sign_in_returning_user_helper(self, mozwebqa):
        self.create_verified_user(mozwebqa.selenium, mozwebqa.timeout)
        mozwebqa.selenium.get('%s/' % mozwebqa.base_url)
        WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
            lambda s: s.find_element_by_id('loggedout').is_displayed())
        mozwebqa.selenium.find_element_by_id('loggedout'). \
            find_element_by_tag_name('button').click()

        browser_id = BrowserID(mozwebqa.selenium, mozwebqa.timeout)
        browser_id.sign_in()
        WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
            lambda s: s.find_element_by_id('loggedin').is_displayed())

    def test_sign_in_returning_user(self, mozwebqa):
        self.create_verified_user(mozwebqa.selenium, mozwebqa.timeout)
        mozwebqa.selenium.get('%s/' % mozwebqa.base_url)
        WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
            lambda s: s.find_element_by_id('loggedout').is_displayed())
        mozwebqa.selenium.find_element_by_id('loggedout'). \
            find_element_by_tag_name('button').click()

        from ...pages.webdriver.sign_in import SignIn
        signin = SignIn(mozwebqa.selenium,
                        mozwebqa.timeout,
                        expect='returning')
        signin.click_sign_in_returning_user()
        WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
            lambda s: s.find_element_by_id('loggedin').is_displayed())

    def test_email_property_returning_user(self, mozwebqa):
        self.create_verified_user(mozwebqa.selenium, mozwebqa.timeout)
        mozwebqa.selenium.get('%s/' % mozwebqa.base_url)
        WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
            lambda s: s.find_element_by_id('loggedout').is_displayed())
        mozwebqa.selenium.find_element_by_id('loggedout'). \
            find_element_by_tag_name('button').click()

        from ...pages.webdriver.sign_in import SignIn
        signin = SignIn(mozwebqa.selenium,
                        mozwebqa.timeout,
                        expect='returning')
        # In the absence of the correct email to assert upon I
        # have used a representative assertion
        assert '@restmail.net' in signin.email
        assert signin.email != ''

    def create_verified_user(self, selenium, timeout):
        restmail_username = 'bidpom_%s' % uuid.uuid1()
        browser_id = BrowserID(selenium, timeout)
        browser_id.sign_in('%s@restmail.net' % restmail_username)
        mail = restmail.get_mail(restmail_username)
        verify_url = re.search(BrowserID.VERIFY_URL_REGEX,
                               mail[0]['text']).group(0)
        selenium.get(verify_url)
        from ...pages.webdriver.verify_email_address import VerifyEmailAddress
        verify_email_address = VerifyEmailAddress(selenium, timeout)
        verify_email_address.verify_email_address('password')
