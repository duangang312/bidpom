#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import selenium


class BrowserID(object):

    def __init__(self, selenium, timeout=60):
        self.selenium = selenium
        self.timeout = timeout
        self._is_rc = isinstance(self.selenium, selenium.selenium)

    def sign_in(self, email, password):
        """Signs in using the specified email address and password."""
        if self._is_rc:
            from pages.rc.sign_in import SignIn
        else:
            from pages.webdriver.sign_in import SignIn
        sign_in = SignIn(self.selenium, timeout=self.timeout)
        sign_in.sign_in(email, password)

    def verify_new_user(self, email):
        """Add a new user via the verify new user workflow."""
        if not self._is_rc:
            from pages.webdriver.sign_in import SignIn
            sign_in = SignIn(self.selenium, timeout=self.timeout)
            sign_in.verify_new_user(email)
