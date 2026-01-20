from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find(self, locator):
        """Найти элемент (с ожиданием)."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        """Кликнуть на элемент."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        return element

    def send_keys(self, locator, text):
        """Ввести текст."""
        element = self.find(locator)
        element.clear()
        element.send_keys(text)
        return self