import path
import sys
import os

directory = path.Path(__file__).abspath()
# setting path
sys.path.append(str(directory.parent.parent.parent.parent.parent))
from importlib.resources import path
import pytest
from WebTest.PageObject.web_page import WebPage
from WebTest.WebInfra.web_driver_factory import WebDriverFactory


class TestWeb(WebDriverFactory):
    def setup_method(self):
        # super().__init__()
        self.login_page = WebPage(self.driver)

    @pytest.mark.webtest
    def test_web_run(self, test_data):
        base_url = test_data["base_url"]
        self.login_page.open_page(base_url)

        for step in test_data["steps"]:
            if step["type"] == "INPUT":
                self.login_page.enter_string(step["xpath"], step["userInput"])
            elif step["type"] == "BUTTON":
                self.login_page.clickButtonByXpath(step["xpath"])
            elif step["type"] == "ASSERTION":
                self.login_page.assertXpath(step["xpath"])

    def teardown_method(self):
        # Cleanup code if needed
        pass


@pytest.mark.webtest
def test_login(test_data):
    run_test = TestWeb()
    run_test.setup_method()
    run_test.test_web_run(test_data)
    run_test.teardown_method()
