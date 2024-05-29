from MobileTest.InitialMobile.mobile_base_function import MobileBaseFunction
from MobileTest.MobileBasePage.mobile_base_pages import MobileBasePages
from selenium.webdriver.common.by import By


class MobilePage(MobileBasePages):
    def __init__(self, driver):
        super().__init__(driver)


    def mobile_click_on_button_by_xpath(self, locatorXpath):
        locator = (By.XPATH, locatorXpath)
        return self.mobile_click_element(locator)
    
    def mobile_enter_text_by_xpath(self, locatorXpath, input_string):
        locator = (By.XPATH, locatorXpath)
        return self.mobile_send_text(locator, input_string)

    def is_close_element_display_by_xpath(self, locatorXpath):
        locator = (By.XPATH, locatorXpath)
        return self.is_element_found(locator)
