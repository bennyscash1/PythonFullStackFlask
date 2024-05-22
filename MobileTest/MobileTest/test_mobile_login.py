import pytest

import GetData
from MobileTest.InitialMobile.mobile_driver_factory import MobileDriverFactory
from MobileTest.MobileFlow.mobile_login_flow import MobileLoginFlow

class MobilaBasicTest(MobileDriverFactory):
    def __init__(self):
        super().__init__()
        self.contact_person = GetData.loaded_data[GetData.VarData.ContactName]
        self.contact_phone = GetData.loaded_data[GetData.VarData.ContactNumber]

    def test_mobile_basic_test(self):
        mobile_login_flow = MobileLoginFlow(self.appium_driver)

        mobile_login_flow.mobile_open_account_frame()

        # Init home page popups
        is_close_icon_display = mobile_login_flow.is_close_icon_display()
        assert is_close_icon_display, "Close icon are not displayed"

def test_contact():
    run_mobile= MobilaBasicTest()
    run_mobile.test_mobile_basic_test()
    pass