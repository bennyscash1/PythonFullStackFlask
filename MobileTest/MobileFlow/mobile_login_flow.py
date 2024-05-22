from MobileTest.MobileFlow.nobile_base_flow import MobileBaseFlow
from  MobileTest.MobileBasePage.mobile_login_page import MobileLoginPage

class MobileLoginFlow(MobileBaseFlow):
    def __init__(self, driver):
        super().__init__(driver)
        self.mobile_login_page_object = MobileLoginPage(driver)

    def mobile_open_account_frame(self):
        self.mobile_login_page_object.click_on_account_icon()
        return self

    def is_close_icon_display(self):
        return self.mobile_login_page_object.is_close_icon_display()
