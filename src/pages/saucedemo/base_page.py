from src.pages.base_page import BasePage

class SauceBasePage(BasePage):
    SAUCE_URL = "https://www.saucedemo.com/"

    def open(self, path=""):
        self.driver.get(f"{self.SAUCE_URL}{path}")
        return self