from time import sleep

import pytest
from selenium.webdriver.common.by import By
from src.pages.saucedemo.base_page import SauceBasePage

def test_login(driver):
    login_page = SauceBasePage(driver)
    login_page.open()
    assert  "Swag Labs" in driver.title

    login_page.send_keys((By.ID, "user-name"), "standard_user")
    login_page.send_keys((By.ID, "password"), "secret_sauce")

    login_page.click((By.ID, "login-button"))

    assert "https://www.saucedemo.com/inventory.html" in driver.current_url





