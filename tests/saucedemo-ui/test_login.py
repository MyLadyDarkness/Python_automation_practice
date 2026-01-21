from time import sleep

import pytest
from selenium.webdriver.common.by import By
from src.pages.saucedemo.base_page import SauceBasePage

def test_login(driver):
    login_page = SauceBasePage(driver)
    login_page.open()
    assert  "Swag Labs" in driver.title

    # log in by empty user
    login_page.send_keys((By.ID, "user-name"), "")
    login_page.send_keys((By.ID, "password"), "")

    login_page.click((By.ID, "login-button"))

    element = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
    assert element.text == "Epic sadface: Username is required"

    # log in by empty password
    login_page.send_keys((By.ID, "user-name"), "s")
    login_page.send_keys((By.ID, "password"), "")

    login_page.click((By.ID, "login-button"))

    element = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
    assert element.text == "Epic sadface: Password is required"

    # log in by not registered user
    login_page.send_keys((By.ID, "user-name"), "s")
    login_page.send_keys((By.ID, "password"), "s")

    login_page.click((By.ID, "login-button"))

    element = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
    assert element.text == "Epic sadface: Username and password do not match any user in this service"

    # log in by locked user
    login_page.send_keys((By.ID, "user-name"), "locked_out_user")
    login_page.send_keys((By.ID, "password"), "secret_sauce")

    login_page.click((By.ID, "login-button"))

    element = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
    assert element.text == "Epic sadface: Sorry, this user has been locked out."

    #log in by standard_user
    login_page.send_keys((By.ID, "user-name"), "standard_user")
    login_page.send_keys((By.ID, "password"), "secret_sauce")

    login_page.click((By.ID, "login-button"))

    #after login
    assert "Swag Labs" in driver.page_source
    assert "inventory.html" in driver.current_url

    assert login_page.find((By.ID, "add-to-cart-sauce-labs-backpack")).text == "Add to cart"





