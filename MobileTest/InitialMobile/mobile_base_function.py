from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pytest

class MobileBaseFunction:
    def __init__(self, driver):
        self.appiumDriver = driver
        self.timeOutInSeconds = 4
        self.maxAttempt = 3

    def is_element_found(self, el):
        wait = WebDriverWait(self.appiumDriver, self.timeOutInSeconds)
        is_element_found = False
        try:
            wait.until(EC.element_to_be_clickable(el))
            is_element_found = True
        except TimeoutException:
            is_element_found = False
        return is_element_found

    def wait_for_element(self, el):
        attempt = 0
        element_click = False

        while attempt < self.maxAttempt:
            if self.is_element_found(el):
                element_click = True
                break
            attempt += 1

        element_details = f"Element {el} search failed within {self.timeOutInSeconds} seconds."
        assert element_click, element_details

    def mobile_click_element(self, el):
        attempt = 0
        element_click = False

        while attempt < self.maxAttempt:
            if self.is_element_found(el):
                self.appiumDriver.find_element(*el).click()
                element_click = True
                break
            attempt += 1

        element_details = f"Element {el} search failed within {self.timeOutInSeconds} seconds."
        assert element_click, element_details

    def fill_text(self, el, text):
        attempt = 0
        element_click = False

        while attempt < self.maxAttempt:
            if self.is_element_found(el):
                self.appiumDriver.find_element(*el).send_keys(text)
                element_click = True
                break
            attempt += 1

        element_details = f"Element {el} sendkeys failed within {self.timeOutInSeconds} seconds."
        assert element_click, element_details

    def mobile_click_back(self):
        self.appiumDriver.back()

    def hide_keyboard(self):
        self.appiumDriver.hide_keyboard()

    def open_status_bar(self):
        self.appiumDriver.open_notifications()

    def close_status_bar(self):
        screen_width = self.appiumDriver.get_window_size()['width']
        screen_height = self.appiumDriver.get_window_size()['height']

        touch_action = TouchAction(self.appiumDriver)
        touch_action.press(x=screen_width / 2, y=screen_height - 10).release().perform()
