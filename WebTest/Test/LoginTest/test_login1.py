

# # directory reach
# import path
# import sys
# import os
# print("hellow world")
# directory = path.Path(__file__).abspath()
# print(directory)
# # setting path
# sys.path.append(str(directory.parent.parent.parent.parent))
# from importlib.resources import path
# import pytest
# from WebTest.Flows.login_flow import LoginFlow
# from WebTest.WebInfra.web_driver_factory import WebDriverFactory


# class TestLoginWeb(WebDriverFactory):
#     def __init__(self):
#         super().__init__()
#     @pytest.mark.webtest    
#     def test_login_web(self):
#         login_flow = LoginFlow(self.driver)
#         with open('user_inputs.txt', 'r') as f:
#             userinputs = f.read().splitlines()
#         login_flow.open_page(True, url=userinputs[0])
#         login_flow.do_login_user_xpath(userinputs[1], userinputs[2], userinputs[3], userinputs[4], userinputs[5])
#     def teardown_method(self):
#         self.driver.quit()
# @pytest.mark.webtest
# def test_login():
#     run_test = TestLoginWeb()
#     run_test.test_login_web()
