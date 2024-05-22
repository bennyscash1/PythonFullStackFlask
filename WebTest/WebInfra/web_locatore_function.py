from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import unittest

class WeblocatoreFunction():
    def __init__(self, driver):
        self.driver = driver
        self.time_out_in_seconds = 6

    def is_element_found(self, by_locator):
        wait = WebDriverWait(self.driver, self.time_out_in_seconds)
        is_element_found = False
        try:
            wait.until(EC.element_to_be_clickable(by_locator))
            self.mark_element(by_locator)
            is_element_found = True
        except TimeoutException:
            is_element_found = False
        return is_element_found

    def wait_for_element_visibility(self, by_locator):
        element_visible = False
        if self.is_element_found(by_locator):
            element_visible = True
            return
        element_details = f"Element {by_locator} search failed within {self.time_out_in_seconds} seconds"
        self.assertTrue(element_visible, element_details)

    def click(self, by_locator):
        element_visible = False
        if self.is_element_found(by_locator):
            web_element = self.driver.find_element(*by_locator)
            web_element.click()
            element_visible = True
            return
        element_details = f"Element {by_locator} click failed within {self.time_out_in_seconds} seconds"
        self.assertTrue(element_visible, element_details)

    def fill_text(self, by_locator, text):
        element_visible = False
        if self.is_element_found(by_locator):
            web_element = self.driver.find_element(*by_locator)
            web_element.click()  # Assuming you want to focus before sending keys
            web_element.send_keys(text)
            element_visible = True
            return
        element_details = f"Element {by_locator} send text failed within {self.time_out_in_seconds} seconds"
        self.assertTrue(element_visible, element_details)

    def switch_to_frame(self):
        self.driver.switch_to.frame(0)

    def is_displayed(self, web_element):
        try:
            self.wait_for_element_visibility(web_element)  # Adjusted to use web_element as locator
            return web_element.is_displayed()
        except WebDriverException:
            return False

    def alert_ok(self):
        self.driver.switch_to.alert.accept()

    def get_text_from_at(self, web_element, attribute):
        self.is_displayed(web_element)
        return web_element.get_attribute(attribute)

    def mark_element(self, by_locator):
        color = "#0000FF"
        element = self.driver.find_element(*by_locator)
        script = f"arguments[0].style.border = '3px solid {color}'"
        self.driver.execute_script(script, element)

# Example of usage
# driver = webdriver.Chrome()  # Or any other browser you're using
# base_functions = BaseFunctions(driver)
# Remember to replace 'webdriver.Chrome()' with your actual WebDriver initialization.
