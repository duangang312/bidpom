#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base import Base

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import time

class SignIn(Base):

    _signed_in_email_locator = (By.XPATH, "//label[input[@checked='checked']]")
    _listed_emails_locator = (By.XPATH, "//label[input[@name='email']]")
    _email_locator = (By.ID, 'email')
    _password_locator = (By.ID, 'password')
    _verify_password_locator = (By.ID, 'vpassword')
    _next_locator = (By.CSS_SELECTOR, 'button.start')
    _sign_in_locator = (By.CSS_SELECTOR, 'button.returning')
    _sign_in_returning_user_locator = (By.ID, 'signInButton')
    _verify_email_locator = (By.ID, 'verify_user')
    _add_another_email_locator = (By.ID, 'useNewEmail')
    _new_email_locator = (By.ID, 'newEmail')
    _add_new_email_locator = (By.ID, 'addNewEmail')
    _check_email_at_locator = (By.CSS_SELECTOR, 'div.contents > p:nth-of-type(1) > strong')

    def __init__(self, selenium, timeout, expect='new'):
        Base.__init__(self, selenium, timeout)

        if self.selenium.title != self._page_title:
            for handle in self.selenium.window_handles:
                self.selenium.switch_to_window(handle)
                WebDriverWait(self.selenium, self.timeout).until(lambda s: s.title)
                if self.selenium.title == self._page_title:
                    break
            else:
                raise Exception('Popup has not loaded')

        if expect == 'new':
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: s.find_element(*self._email_locator).is_displayed())
        elif expect == 'returning':
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: s.find_element(
                    *self._sign_in_returning_user_locator).is_displayed())
            time.sleep(2)
        else:
            raise Exception('Unknown expect value: %s' % expect)

    def close_window(self):
        self.selenium.close()

    @property
    def signed_in_email(self):
        """Get the value of the email that is currently signed in."""
        return self.selenium.find_element(*self._signed_in_email_locator).text

    @property
    def emails(self):
        """ Lists the emails for the returning user """
        return [element.text for element in self.selenium.find_elements(*self._listed_emails_locator)]

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
    def new_email(self):
        """Get the value of the new email field."""
        return self.selenium.find_element(*self._new_email_locator).text

    @new_email.setter
    def new_email(self, value):
        """Set the value of the new email field."""
        email = self.selenium.find_element(*self._new_email_locator)
        email.clear()
        email.send_keys(value)

    @property
    def selected_email(self):
        """Return the value of the selected email of returning user's multiple emails"""
        return self.signed_in_email

    def select_email_checkbox(self, value):
        """ Select email from the returning user's multiple emails """
        checkbox = self.selenium.find_element(By.CSS_SELECTOR, "input[value='%s']" % value)
        checkbox.click()

    def check_email_at_address(self):
        return self.selenium.find_element(*self._check_email_at_locator).text

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

    @property
    def verify_password(self):
        """Get the value of the verify password field."""
        return self.selenium.find_element(*self._verify_password_locator).text

    @password.setter
    def verify_password(self, value):
        """Set the value of the verify password field."""
        password = self.selenium.find_element(*self._verify_password_locator)
        password.clear()
        password.send_keys(value)

    def click_next(self, expect='password'):
        """Clicks the 'next' button."""
        self.selenium.find_element(*self._next_locator).click()
        if expect == 'password':
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: s.find_element(
                    *self._password_locator).is_displayed())
        elif expect == 'verify':
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: s.find_element(
                    *self._verify_email_locator).is_displayed())
        else:
            raise Exception('Unknown expect value: %s' % expect)

    def click_sign_in(self):
        """Clicks the 'sign in' button."""
        self.selenium.find_element(*self._sign_in_locator).click()
        self.switch_to_main_window()

    def click_sign_in_returning_user(self):
        """Clicks the 'sign in' button."""
        self.selenium.find_element(
            *self._sign_in_returning_user_locator).click()
        self.switch_to_main_window()

    def click_verify_email(self):
        """Clicks 'verify email' button."""
        self.selenium.find_element(*self._verify_email_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(
                *self._check_email_at_locator).is_displayed())

    def click_add_another_email_address(self):
        """Clicks 'add another email' button."""
        self.selenium.find_element(*self._add_another_email_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(
                *self._add_new_email_locator).is_displayed())

    def click_add_new_email(self):
        """Clicks 'Add' button to insert new email address."""
        self.selenium.find_element(*self._add_new_email_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(
                *self._check_email_at_locator).is_displayed())

    def sign_in(self, email, password):
        """Signs in using the specified email address and password."""
        self.email = email
        self.click_next(expect='password')
        self.password = password
        self.click_sign_in()

    def sign_in_new_user(self, email, password):
        """Requests verification email using the specified email address."""
        self.email = email
        self.click_next(expect='verify')
        self.password = password
        self.verify_password = password
        self.click_verify_email()
        self.close_window()
        self.switch_to_main_window()

    def sign_in_returning_user(self):
        """Signs in with the stored user."""
        self.click_sign_in_returning_user()

    def sign_in_add_another_email(self, email):
        self.click_add_another_email_address()
        self.new_email = email
        self.click_add_new_email()
        self.close_window()
        self.switch_to_main_window()
