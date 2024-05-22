import os
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.ie.service import Service as IEService


class WebDriverFactory:
    def __init__(self, browser_type='Chrome'):
        self.time_out_in_seconds = 20
        self.driver = self.create_webdriver(browser_type)
        self.driver.maximize_window()

    @staticmethod
    def close_running_chromedriver_processes():
        try:
            subprocess.call(['taskkill', '/F', '/IM', 'chromedriver.exe', '/T'])
        except Exception as ex:
            print(f"An error occurred while killing Chromedriver processes: {ex}")

    @staticmethod
    def remove_chromedriver():
        WebDriverFactory.close_running_chromedriver_processes()
        chrome_driver_path = os.path.join(os.getcwd(), 'chromedriver.exe')
        try:
            os.chmod(chrome_driver_path, 0o777)  # Make sure the file is writable
            os.remove(chrome_driver_path)
            print(f"Chromedriver removed successfully from {chrome_driver_path}")

        except Exception as ex:
            print(f"An error occurred while removing Chromedriver: {ex}")

    def create_webdriver(self, browser_type):
        if browser_type == 'Chrome':
            return self.chrome_driver()
        elif browser_type == 'Firefox':
            return self.firefox_driver()
        elif browser_type == 'IE':
            return self.ie_driver()
        else:
            return self.chrome_driver()

    @staticmethod
    def chrome_driver():
        #WebDriverFactory.remove_chromedriver()
        driver = webdriver.Chrome()
        return driver

    # @staticmethod
    # def firefox_driver():
    #     service = FirefoxService(GeckoDriverManager().install())
    #     driver = webdriver.Firefox(service=service)
    #     return driver
    #
    # @staticmethod
    # def ie_driver():
    #     service = IEService(IEDriverManager().install())
    #     driver = webdriver.Ie(service=service)
    #     return driver

    def dispose(self):
        self.driver.close()

# Example of usage
# factory = WebDriverFactory('Chrome')
# driver = factory.driver
# Remember to replace 'Chrome' with your desired browser type.
