#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import selenium


class BrowserID(object):

    def __init__(self, selenium, timeout=60):
        self.selenium = selenium
        self.timeout = timeout

    @property
    def __is_rc(self):
        try:
            return isinstance(self.selenium, selenium.selenium)
        except:
            return False

    def sign_in(self, email, password):
        """Signs in using the specified email address and password."""
        if self.__is_rc:
            from pages.rc.sign_in import SignIn
        else:
            from pages.webdriver.sign_in import SignIn
        sign_in = SignIn(self.selenium, timeout=self.timeout)
        sign_in.sign_in(email, password)

    def verify_new_user(self, email):
        """Add a new user via the verify new user workflow."""
        if self.__is_rc:
            raise Exception("Not yet supported for Selenium RC")
        else:
            from pages.webdriver.sign_in import SignIn
        sign_in = SignIn(self.selenium, timeout=self.timeout)
        sign_in.verify_new_user(email)

    def verify_email_address(self, password):
        """Add a new user via the verify new user workflow."""
        if self.__is_rc:
            raise Exception("Not yet supported for Selenium RC")
        else:
            from pages.webdriver.verify_email_address import VerifyEmailAddress

        verify_email_address = VerifyEmailAddress(self.selenium, timeout=self.timeout)
        verify_email_address.enter_passwords_and_verify_account(password)
