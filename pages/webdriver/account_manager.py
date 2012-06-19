#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base import Base

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class AccountManager(Base):

    _content_locator = (By.ID, 'content')
    _email_locator = (By.CSS_SELECTOR, '#emailList .email')
    _edit_password_button_locator = (By.CSS_SELECTOR, '#edit_password button.edit')
    _edit_password_form_locator = (By.ID, 'edit_password_form')
    _old_password_field_locator = (By.ID, 'old_password')
    _new_password_field_locator = (By.ID, 'new_password')
    _change_password_done_locator = (By.ID, 'changePassword')

    _sign_out_locator = (By.CSS_SELECTOR, 'a.signOut')

    def __init__(self, selenium, timeout, expect='success'):
        Base.__init__(self, selenium, timeout)

        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(*self._content_locator).is_displayed(),
            'Main content div did not appear before timeout')

    @property
    def email(self):
        return [web_element.text for web_element in self.selenium.find_elements(*self._email_locator)]

    def click_edit_password(self):
        """Click edit password to show the new/old password fields"""
        self.selenium.find_element(*self._edit_password_button_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: self.is_edit_password_form_visible,
            'Edit password fields were not shown before timeout')

    @property
    def old_password(self):
        """Get the value of the password field."""
        return self.selenium.find_element(*self._old_password_field_locator).text

    @old_password.setter
    def old_password(self, value):
        """Set the value of the password field."""
        password = self.selenium.find_element(*self._old_password_field_locator)
        password.clear()
        password.send_keys(value)

    @property
    def new_password(self):
        """Get the value of the password field."""
        return self.selenium.find_element(*self._new_password_field_locator).text

    @new_password.setter
    def new_password(self, value):
        """Set the value of the password field."""
        password = self.selenium.find_element(*self._new_password_field_locator)
        password.clear()
        password.send_keys(value)

    def click_password_done(self):
        """Click password done to save the new password"""
        self.selenium.find_element(*self._change_password_done_locator).click()        
        WebDriverWait(self.selenium, self.timeout).until(lambda s: not self.is_edit_password_form_visible)

    @property
    def is_edit_password_form_visible(self):
        return self.selenium.find_element(*self._edit_password_form_locator).is_displayed()

    def click_sign_out(self):
        self.selenium.find_element(*self._sign_out_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(lambda s: len(s.find_elements(*self._content_locator)) == 0)
