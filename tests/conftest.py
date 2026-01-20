import pytest
from selenium import webdriver

@pytest.fixture(scope="function", autouse=True)
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()
