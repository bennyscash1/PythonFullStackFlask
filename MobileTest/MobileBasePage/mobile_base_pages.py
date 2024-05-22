from MobileTest.InitialMobile.mobile_base_function import MobileBaseFunction


class MobileBasePages(MobileBaseFunction):
    def __init__(self, appium_driver):
        super().__init__(appium_driver)
        self.appium_driver = appium_driver
        self.max_attempt = 2