from WebTest.WebInfra.web_locatore_function import WeblocatoreFunction


class BasePages(WeblocatoreFunction):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.time_out_in_seconds = 6

