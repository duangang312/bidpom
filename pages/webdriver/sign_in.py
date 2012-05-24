#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base import Base

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class SignIn(Base):

    _email_locator = (By.ID, 'email')
    _email_label_locator = (By.CSS_SELECTOR, "label[for='email_0']")
    _password_locator = (By.ID, 'password')
    _next_locator = (By.CSS_SELECTOR, 'button.start')
    _sign_in_locator = (By.CSS_SELECTOR, 'button.returning')
    _sign_in_returning_user_locator = (By.ID, 'signInButton')
    _verify_email_locator = (By.CSS_SELECTOR, 'button.newuser')
    _content_header_locator = (By.CSS_SELECTOR, 'div.contents h2')

    def __init__(self, *args, **kwargs):
        Base.__init__(self, *args, **kwargs)

    @property
    def email(self):
        """Get the value of the email field."""
        return self.selenium.find_element(*self._email_locator).text

    @email.setter
    def email(self, value):
        """Set the value of the email field."""
        email = self.selenium.find_element(*self._email_locator)
        email.clear()
        email.send_keys(value)

    @property
    def password(self):
        """Get the value of the password field."""
        return self.selenium.find_element(*self._password_locator).text

    @password.setter
    def password(self, value):
        """Set the value of the password field."""
        password = self.selenium.find_element(*self._password_locator)
        password.clear()
        password.send_keys(value)

    def click_next(self):
        """Clicks the 'next' button."""
        self.selenium.find_element(*self._next_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: not s.find_element(*self._next_locator).is_displayed())

    def click_sign_in(self):
        """Clicks the 'Sign In' button."""
        self.selenium.find_element(*self._sign_in_locator).click()
        self.switch_to_main_window()

    def click_sign_in_returning_user(self):
        """Clicks the 'Sign In' button."""
        self.selenium.find_element(*self._sign_in_returning_user_locator).click()
        self.switch_to_main_window()

    def click_verify_email(self):
        """Clicks verify email button and wait for success confirmation"""
        self.selenium.find_element(*self._verify_email_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(*self._content_header_locator).text == 'Check your email!')

    def close_persona_window(self):
        self.selenium.close()

    def sign_in(self, email, password):
        """Signs in using the specified email address and password."""

        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(*self._email_locator).is_displayed())

        self.email = email
        self.click_next()
        self.password = password
        self.click_sign_in()

    def sign_in_new_user(self, email):
        """Enter an email address and click Verify Email button """

        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(*self._email_locator).is_displayed())

        self.email = email
        self.click_next()
        self.click_verify_email()
        self.close_persona_window()
        self.switch_to_main_window()

    def sign_in_returning_user(self, email):
        """Sign in a user who already has an account"""

        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(*self._sign_in_returning_user_locator).is_displayed())

        email_label = self.selenium.find_element(*self._email_label_locator)
        assert email_label.text == email
        self.click_sign_in_returning_user()
