from time import sleep

import pytest
from selenium.webdriver.common.by import By
from src.pages.saucedemo.base_page import SauceBasePage


@pytest.mark.parametrize("login, password, error_msg" ,
                         [
                             ("", "", "Epic sadface: Username is required"),
                             ("s", "", "Epic sadface: Password is required"),
                             ("s", "s", "Epic sadface: Username and password do not match any user in this service"),
                             ("locked_out_user", "secret_sauce", "Epic sadface: Sorry, this user has been locked out.")
                          ],

                        ids=[
                                "empty_login_and_password",
                                "empty_password_only",
                                "not_registered_user",
                                "locked_out_user"
                            ]
                         )

def test_login_error(driver, login, password, error_msg):
    login_page = SauceBasePage(driver)
    login_page.open()
    assert  "Swag Labs" in driver.title

    login_page.login(login)
    login_page.password(password)
    login_page.click((By.ID, "login-button"))
    login_page.assertions_error(error_msg)


@pytest.mark.parametrize("login, password",
                         [
                             ("standard_user", "secret_sauce"),
                             ("problem_user", "secret_sauce"),
                             ("performance_glitch_user", "secret_sauce"),
                             ("error_user", "secret_sauce"),
                             ("visual_user", "secret_sauce")
                         ],

                         ids=[
                             "standard_user",
                             "problem_user",
                             "performance_glitch_user",
                             "error_user",
                             "visual_user"
                         ]
                         )

def test_login_success(driver, login, password):
    login_page = SauceBasePage(driver)
    login_page.open()
    assert "Swag Labs" in driver.title

    login_page.login(login)
    login_page.password(password)
    login_page.click((By.ID, "login-button"))
    login_page.assertions_ok()
    login_page.logout()

    # # log in by empty user
    # login_page.send_keys((By.ID, "user-name"), "")
    # login_page.send_keys((By.ID, "password"), "")
    #
    # login_page.click((By.ID, "login-button"))
    #
    # element = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
    # assert element.text == "Epic sadface: Username is required"
    #
    # # log in by empty password
    # login_page.send_keys((By.ID, "user-name"), "s")
    # login_page.send_keys((By.ID, "password"), "")
    #
    # login_page.click((By.ID, "login-button"))
    #
    # element = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
    # assert element.text == "Epic sadface: Password is required"
    #
    # # log in by not registered user
    # login_page.send_keys((By.ID, "user-name"), "s")
    # login_page.send_keys((By.ID, "password"), "s")
    #
    # login_page.click((By.ID, "login-button"))
    #
    # element = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
    # assert element.text == "Epic sadface: Username and password do not match any user in this service"
    #
    # # log in by locked user
    # login_page.send_keys((By.ID, "user-name"), "locked_out_user")
    # login_page.send_keys((By.ID, "password"), "secret_sauce")
    #
    # login_page.click((By.ID, "login-button"))
    #
    # element = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
    # assert element.text == "Epic sadface: Sorry, this user has been locked out."
    #
    # #log in by standard_user
    # login_page.send_keys((By.ID, "user-name"), "standard_user")
    # login_page.send_keys((By.ID, "password"), "secret_sauce")
    #
    # login_page.click((By.ID, "login-button"))
    #
    # #after login
    # assert "Swag Labs" in driver.page_source
    # assert "inventory.html" in driver.current_url
    #
    # assert login_page.find((By.ID, "add-to-cart-sauce-labs-backpack")).text == "Add to cart"





