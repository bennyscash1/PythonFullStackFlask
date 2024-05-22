import path
import sys
import os

print("hellow world")
directory = path.Path(__file__).abspath()
print(directory)
# setting path
sys.path.append(str(directory.parent.parent.parent.parent))
from importlib.resources import path
import pytest
from WebTest.PageObject.login_page import LoginPage
from WebTest.WebInfra.web_driver_factory import WebDriverFactory

class TestLoginWeb(WebDriverFactory):
    def setup_method(self):
        super().__init__()
        self.login_page = LoginPage(self.driver)

    @pytest.mark.webtest    
    def test_login_web(self):
        with open(os.path.join(os.path.dirname(directory), 'user_inputs.txt'), 'r') as f:
            userinputs = f.read().splitlines()

        base_url = userinputs[0]
        self.login_page.open_page(True, url=base_url)

        index = 1
        while index < len(userinputs):
            xpath = userinputs[index]
            if index + 1 < len(userinputs) and not userinputs[index + 1].startswith('/'):
                input_value = userinputs[index + 1]
                if input_value:  # Non-empty input value indicates a text entry
                    self.login_page.enter_string(xpath, input_value)
                    index += 2
                # else:
                #     self.login_page.clickButtonByXpath(xpath)
                #     index += 1
            else:
                self.login_page.clickButtonByXpath(xpath)
                index += 1

    # def teardown_method(self):
    #     # Do not close the browser here
    #     pass

@pytest.mark.webtest
def test_login():
    run_test = TestLoginWeb()
    run_test.setup_method()
    run_test.test_login_web()
    # Commenting out the teardown call to keep the browser open
    # run_test.teardown_method()
