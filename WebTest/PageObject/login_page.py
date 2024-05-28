from selenium.webdriver.common.by import By
from WebTest.PageObject.base_pages import BasePages


class LoginPage(BasePages):

    def __init__(self, driver):
        super().__init__(driver)    
       # self.driver = driver 
    
    def open_page(self, navigate_to_logon_screen=True, url=None):
        if navigate_to_logon_screen and url is not None:
            self.driver.get(url)
        return self
    ##Input data
    def enter_string(self, xpath, textInput):
        locator = (By.XPATH, xpath)
        return self.fill_text(locator, textInput)
    
    def clickButtonByXpath(self, xpath):
        locator = (By.XPATH, xpath)
        return self.click(locator)
    
    def assertXpath(self, xpath):
        locator = (By.XPATH, xpath)
        return self.is_element_found(locator)
    ##
    def enter_email(self, email):
        self.fill_text(self.m_user_name_input_field, email)
        return self

    def enter_password(self, password):
        self.fill_text(self.m_password_input_field, password)
        return self

    def click_on_submit_button(self):
        self.click(self.m_submit_button)
        return self

    def is_home_page_displayed(self):
        self.wait_for_element_visibility(self.m_home_page_logo_by)
        return True
