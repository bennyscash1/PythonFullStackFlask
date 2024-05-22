from MobileTest.MobileBasePage.mobile_base_pages import MobileBasePages


class MobileLoginPage(MobileBasePages):
    def __init__(self, driver):
        super().__init__(driver)
        self.m_account_icon_by = ("xpath", "//android.widget.ImageView[@resource-id='com.google.android.contacts:id/og_apd_internal_image_view']")
        self.m_close_icon_by = ("id", "com.google.android.contacts:id/og_header_close_button")

    def click_on_account_icon(self):
        self.mobile_click_element(self.m_account_icon_by)
        return self

    def is_close_icon_display(self):
        self.wait_for_element(self.m_close_icon_by)
        return True
