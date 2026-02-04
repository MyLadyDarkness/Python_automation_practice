from src.pages.base_page import BasePage
from selenium.webdriver.common.by import By

class SauceBasePage(BasePage):
    SAUCE_URL = "https://www.saucedemo.com/"

    def open(self, path=""):
        self.driver.get(f"{self.SAUCE_URL}{path}")
        return self

    def standard_login(self):
        self.send_keys((By.ID, "user-name"), "standard_user")
        self.send_keys((By.ID, "password"), "secret_sauce")
        self.click((By.ID, "login-button"))

    def login(self, login):
        self.send_keys((By.ID, "user-name"), login)

    def password(self, password):
        self.send_keys((By.ID, "password"), password)

    def assertions_error(self, error_msg):
        assert self.find((By.CSS_SELECTOR, "h3[data-test='error']")).text == error_msg

    def assertions_ok(self):
        assert "/inventory" in self.driver.current_url

    def logout(self):
        self.click((By.ID, "react-burger-menu-btn"))
        self.click((By.ID, "logout_sidebar_link"))
        assert self.find((By.ID, "login-button"))
