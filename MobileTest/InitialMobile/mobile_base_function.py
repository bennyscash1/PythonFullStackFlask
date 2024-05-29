from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import pytest

class MobileBaseFunction:
    def __init__(self, driver):
        self.appiumDriver = driver
        self.timeOutInSeconds = 4
        self.maxAttempt = 3

    def is_element_found(self, el):
        attempt = 0
        element_locator_found = False

        while attempt < self.maxAttempt:
            wait = WebDriverWait(self.appiumDriver, self.timeOutInSeconds)           
            try:
                self.appiumDriver.find_element(*el)  
                wait.until(EC.presence_of_element_located(el))
                element_locator_found = True
                break
            except TimeoutException:
                attempt += 1
        return element_locator_found

    def wait_for_element(self, el):
        element_click = False

        if self.is_element_found(el):
            element_click = True

        element_details = f"Element {el} search failed within {self.timeOutInSeconds} seconds."
        assert element_click, element_details

    def mobile_click_element(self, el):
        if self.is_element_found(el):
            self.appiumDriver.find_element(*el).click()
            element_click = True
        else:
            element_click = False

        element_details = f"Element {el} search failed within {self.timeOutInSeconds} seconds."
        assert element_click, element_details

    def mobile_send_text(self, el, text):
        if self.is_element_found(el):
            self.appiumDriver.find_element(*el).send_keys(text)
            element_click = True
        else:
            element_click = False

        element_details = f"Element {el} sendkeys failed within {self.timeOutInSeconds} seconds."
        assert element_click, element_details

    def mobile_click_back(self):
        self.appiumDriver.back()

    def hide_keyboard(self):
        self.appiumDriver.hide_keyboard()

    def open_status_bar(self):
        self.appiumDriver.open_notifications()

    # def close_status_bar(self):
    #     screen_width = self.appiumDriver.get_window_size()['width']
    #     screen_height = self.appiumDriver.get_window_size()['height']

    #     touch_action = TouchAction(self.appiumDriver)
    #     touch_action.press(x=screen_width / 2, y=screen_height - 10).release().perform()
