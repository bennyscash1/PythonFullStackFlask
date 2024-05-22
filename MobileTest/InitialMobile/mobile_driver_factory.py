from appium import webdriver, options
from appium.options.android import UiAutomator2Options
from appium.options.common import AppiumOptions
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

import GetData


class MobileDriverFactory:
    def __init__(self):
        self.appium_driver = self.init_appium_driver()

    def create_appium_options(self):
        # Assuming GetData.loaded_data and GetData.VarData are defined and provide necessary configuration
        appPackage = GetData.loaded_data[GetData.VarData.AppPackage]
        appActivity = GetData.loaded_data[GetData.VarData.AppActivity]
        options = AppiumOptions()
        options.set_capability('platformName', 'Android')
        options.set_capability('deviceName', 'bennys9')
        options.set_capability('appPackage', appPackage)
        options.set_capability('appActivity', appActivity)
        options.set_capability('udid', '43bd5a1b')
        return options
    def init_appium_driver(self):
        options = self.create_appium_options()

        self.appium_driver = WebDriver(command_executor='http://127.0.0.1:4723/wd/hub', options=options)
        return self.appium_driver


