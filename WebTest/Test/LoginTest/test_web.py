import path
import sys
import os

print("hellow world")
directory = path.Path(__file__).abspath()
print(directory)
# setting path
sys.path.append(str(directory.parent.parent.parent.parent.parent))
from importlib.resources import path
import pytest
from WebTest.PageObject.web_page import WebPage
from WebTest.WebInfra.web_driver_factory import WebDriverFactory

class TestWeb(WebDriverFactory):
    def setup_method(self):
        super().__init__()
        self.login_page = WebPage(self.driver)

    @pytest.mark.webtest    
    def test_web_run(self):
        with open(os.path.join(os.path.dirname(directory), 'user_inputs.txt'), 'r') as f:
            userinputs = f.read().splitlines()

        base_url = userinputs[0]
        self.login_page.open_page(True, url=base_url)

        index = 1
        while index < len(userinputs):
            locatorsX = userinputs[index]
            
            # Handling InputXpath
            if  locatorsX is not None:
                xpath = locatorsX.split(": ")[1].split(", ")[0]
                
                if locatorsX.startswith('InputXpath') :
                    input_value = locatorsX.split(": ")[1].split(", ")[1]# Non-empty input value indicates a text entry
                    ret = self.login_page.enter_string(xpath, input_value)
                    index += 1

                # Handling ButtonAction
                elif locatorsX.startswith('ButtonAction'):
                    xpath = locatorsX.split(": ")[1]
                    self.login_page.clickButtonByXpath(xpath)
                    index += 1

                # Handling AssertXpath
                elif locatorsX.startswith('AssertXpath'):
                    xpath = locatorsX.split(": ")[1]
                    self.login_page.assertXpath(xpath)
                    index += 1

                # else:


    # def teardown_method(self):
    #     # Do not close the browser here
    #     pass

@pytest.mark.webtest
def test_login():
    run_test = TestWeb()
    run_test.setup_method()
    run_test.test_web_run()
    # Commenting out the teardown call to keep the browser open
    # run_test.teardown_method()
