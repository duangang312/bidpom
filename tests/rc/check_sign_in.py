#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import uuid

import pytest


from ... import BrowserID
from .. import restmail
from base import BaseTest


@pytest.mark.nondestructive
class TestSignIn(BaseTest):

    def test_sign_in_helper(self, mozwebqa):
        browser_id = BrowserID(mozwebqa.selenium, mozwebqa.timeout)
        browser_id.sign_in(mozwebqa.email, mozwebqa.password)

        logout_locator = 'css=#loggedin a'
        mozwebqa.wait_for_element_visible(mozwebqa, logout_locator)
        assert mozwebqa.selenium.is_visible(logout_locator)

    def test_sign_in(self, mozwebqa):
        from ...pages.rc.sign_in import SignIn
        signin = SignIn(mozwebqa.selenium, mozwebqa.timeout, expect='new')
        signin.email = mozwebqa.email
        signin.click_next(expect='password')
        signin.password = mozwebqa.password
        signin.click_sign_in()

        logout_locator = 'css=#loggedin a'
        mozwebqa.wait_for_element_visible(mozwebqa, logout_locator)
        assert mozwebqa.selenium.is_visible(logout_locator)

    @pytest.mark.travis
    def test_sign_in_new_user_helper(self, mozwebqa):
        restmail_username = 'bidpom_%s' % uuid.uuid1()
        email = '%s@restmail.net' % restmail_username

        from ...pages.rc.sign_in import SignIn
        signin = SignIn(mozwebqa.selenium, mozwebqa.timeout, expect='new')
        print 'signing in as %s' % email
        signin.sign_in_new_user(email, 'password')
        mail = restmail.get_mail(restmail_username)
        assert 'Click to confirm this email address' in mail[0]['text']

    @pytest.mark.travis
    def test_sign_in_new_user(self, mozwebqa):
        restmail_username = 'bidpom_%s' % uuid.uuid1()
        email = '%s@restmail.net' % restmail_username
        password = 'password'

        from ...pages.rc.sign_in import SignIn
        signin = SignIn(mozwebqa.selenium, mozwebqa.timeout, expect='new')
        print 'signing in as %s' % email
        signin.email = email
        signin.click_next(expect='verify')
        signin.password = password
        signin.verify_password = password
        signin.click_verify_email()
        assert signin.check_email_at_address == email

        signin.close_window()
        signin.switch_to_main_window()
        mail = restmail.get_mail(restmail_username)
        assert 'Click to confirm this email address' in mail[0]['text']

    @pytest.mark.travis
    def test_sign_in_returning_user(self, mozwebqa):
        self.create_verified_user(mozwebqa.selenium, mozwebqa.timeout)
        mozwebqa.selenium.open('%s/' % mozwebqa.base_url)
        logout_locator = 'css=#loggedin a'
        mozwebqa.wait_for_element_visible(mozwebqa, logout_locator)
        assert mozwebqa.selenium.is_visible(logout_locator)
