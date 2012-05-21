#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from selenium.webdriver.support.ui import WebDriverWait


class TestVerifyEmailAddress:

    #@pytest.mark.xfail(reason='This test requires a user account in pre-verified state')
    def test_verify_email_address_helper(self, mozwebqa):
        # Navigate to path given in user's email, eg:
        mozwebqa.selenium.get('https://browserid.org/verify_email_address?token=aww7pV5ZpY339GThG92kUiiPO5sCm9EBB9DM8CjgVhONbCsC')
        
        from ... import BrowserID
        browser_id = BrowserID(mozwebqa.selenium, mozwebqa.timeout)
        
        browser_id.verify_email_address(mozwebqa.password)

        WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
            lambda s: s.find_element_by_id('congrats').is_displayed())

    #@pytest.mark.xfail(reason='This test requires a user account in pre-verified state')
    def test_sign_in(self, mozwebqa):
        # Navigate to path given in user's email
        mozwebqa.selenium.get('https://browserid.org/verify_email_address?token=d3QYv7nKjNu94HJZvbN9MbuV1Acs4b25zWQ9eHFJlrGC9OHU')

        from ...pages.webdriver.verify_email_address import VerifyEmailAddress
        verify_email_address = VerifyEmailAddress(mozwebqa.selenium, mozwebqa.timeout)

        verify_email_address.password = mozwebqa.password
        verify_email_address.verify_password = mozwebqa.password
        verify_email_address.click_finish()

        WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
            lambda s: s.find_element_by_id('congrats').is_displayed())
