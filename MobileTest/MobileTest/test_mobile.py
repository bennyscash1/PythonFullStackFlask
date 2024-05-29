import path
import sys
import os
import time

directory = path.Path(__file__).abspath()
print(directory)
sys.path.append(str(directory.parent.parent.parent.parent))
from importlib.resources import path
import pytest
from appium import webdriver
from MobileTest.MobileBasePage.mobile_page import MobilePage
from appium import webdriver, options
from appium.options.android import UiAutomator2Options
from appium.options.common import AppiumOptions
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class TestMobile:
    
    def setup_method(self):
        directory = os.path.abspath(os.path.dirname(__file__))

        with open(os.path.join(directory, 'user_inputs.txt'), 'r') as f:
            userinputs = f.read().splitlines()

        self.app_package = userinputs[0].split(": ")[1]
        self.app_activity = userinputs[1].split(": ")[1]
        self.udid = userinputs[2].split(": ")[1]

        # Set up Appium options
        options = AppiumOptions()
        options.set_capability('platformName', 'Android')
        options.set_capability('deviceName', 'bennys9')
        options.set_capability('automationName', "UiAutomator2")
        options.set_capability('appPackage', self.app_package)
        options.set_capability('appActivity', self.app_activity)
        options.set_capability('udid', self.udid)

        appium_server = 'http://127.0.0.1:4723/wd/hub'
        self.driver = WebDriver(command_executor=appium_server, options=options)
        print(appium_server + " run successfully")
        time.sleep(3)  # Sleep for 5 seconds
        self.mobile_page = MobilePage(driver=self.driver)

    @pytest.mark.mobiletest
    def test_mobile_run(self):
        directory = os.path.abspath(os.path.dirname(__file__))

        with open(os.path.join(directory, 'user_inputs.txt'), 'r') as f:
            userinputs = f.read().splitlines()

        index = 3
        while index < len(userinputs):
            locatorsX = userinputs[index]

            if locatorsX is not None:
                xpath = locatorsX.split(": ")[1].split(", ")[0]

                if locatorsX.startswith('InputXpath'):
                    input_value = locatorsX.split(": ")[1].split(", ")[1]  # Non-empty input value indicates a text entry
                    self.mobile_page.mobile_enter_text_by_xpath(xpath, input_value)
                    index += 1

                elif locatorsX.startswith('ButtonAction'):
                    self.mobile_page.mobile_click_on_button_by_xpath(xpath)
                    index += 1

                elif locatorsX.startswith('AssertXpath'):
                    self.mobile_page.is_close_element_display_by_xpath(xpath)
                    index += 1

    # Uncomment if you want to close the app after the test
    # def teardown_method(self):
    #     self.driver.quit()

@pytest.mark.mobiletest
def test_mobile():
    TestMobile.setup_method()  
    TestMobile.test_mobile_run()
