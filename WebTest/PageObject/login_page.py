from selenium.webdriver.common.by import By
from WebTest.PageObject.base_pages import BasePages


class LoginPage(BasePages):

    def __init__(self, driver):
        super().__init__(driver)    
       # self.driver = driver 
        self.m_user_name_input_field = (By.XPATH, "//input[@id='username']")
        self.m_password_input_field = (By.XPATH, "//input[@id='password']")
        self.m_submit_button = (By.XPATH, "//button[@id='submit']")
        self.m_home_page_logo_by = (By.XPATH, "//h1[normalize-space()='Logged In Successfully']")
    
    def open_page(self, navigate_to_logon_screen=True, url=None):
        if navigate_to_logon_screen and url is not None:
            self.driver.get(url)
        return self
    ##Input data
    def enter_string(self, xpath, textInput):
        locator = (By.XPATH, xpath)
        self.fill_text(locator, textInput)
        return self
    
    def clickButtonByXpath(self, xpath):
        locator = (By.XPATH, xpath)
        self.click(locator)
        return self
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
