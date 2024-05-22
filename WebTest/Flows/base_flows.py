from selenium.webdriver.common.by import By

from WebTest.PageObject.base_pages import BasePages


# Assuming BaseTest is defined somewhere within your project

class BaseFlows():

    def __init__(self, driver):
        self.driver = driver
        self.base_pages = BasePages(driver)

    def get_current_url(self):
        return self.driver.current_url

    def navigate_to_url(self, url):
        self.driver.get(url)

# Example of usage:
# driver = webdriver.Chrome()  # Or any other browser
# base_flows = BaseFlows(driver)
# base_flows.navigate_to_url("https://example.com")
# print(base_flows.get_current_url())
