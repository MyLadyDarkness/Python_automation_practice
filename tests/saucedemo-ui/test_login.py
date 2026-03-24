import pytest
from selenium.webdriver.common.by import By
from src.pages.saucedemo.base_page import SauceBasePage
import allure


@pytest.mark.smoke
@allure.title("Вход в систему. НЕГАТИВНЫЙ ТСЕТ")
@allure.feature("LOGIN")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("login, password, error_msg",
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

    with allure.step("1. Открытие страницы"):
        login_page.open()
        assert "Swag Labs" in driver.title

    screenshot = driver.get_screenshot_as_jpg()
    allure.attach(screenshot, name="Страница открыта", attachment_type=allure.attachment_type.JPG)

    login_page.login(login)
    login_page.password(password)

    with allure.step("2. Вход в систему"):
        login_page.click((By.ID, "login-button"))

    with allure.step("3. Сообщение об ошибке"):
        login_page.assertions_error(error_msg)

    allure.attach(f"Ошибка: {error_msg}", screenshot, name="Ошибка", attachment_type=allure.attachment_type.TEXT)


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
