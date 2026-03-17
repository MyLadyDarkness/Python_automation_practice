from selenium.webdriver.common.by import By
from src.pages.saucedemo.base_page import SauceBasePage
from selenium.common.exceptions import NoSuchElementException
import pytest

from src.utils.checkout_information import checkout_information


class CartPage(SauceBasePage):

    def count_cart_items(self):
        cart_items = self.driver.find_elements(By.CSS_SELECTOR, "[class*=cart_button][name*=remove]")
        return len(cart_items)

    def get_cart_item_details(self):
        """Возвращает список товаров в корзине."""
        items = []
        cart_items = self.driver.find_elements(By.CLASS_NAME, "cart_item")

        for element in cart_items:
            items.append({
                "name": element.find_element(By.CLASS_NAME, "inventory_item_name").text,
                "price": element.find_element(By.CLASS_NAME, "inventory_item_price").text,
                "description": element.find_element(By.CLASS_NAME, "inventory_item_desc").text
            })

        return items

    def remove_from_cart(self):
        all_items_buttons = self.driver.find_element(By.CSS_SELECTOR, "[id*='remove']")
        all_items_buttons.click()

        with pytest.raises(NoSuchElementException):
            self.driver.find_element(By.CSS_SELECTOR, "[id*='remove']")

    def checkout(self):
        cart_items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
        if cart_items:
            self.find((By.ID, "checkout")).click()

        else:
            raise Exception("Cannot checkout: cart is empty")

    def fill_checkout_information(self):
        checkout_info = checkout_information()
        self.driver.find_element(By.ID, "first-name").send_keys(checkout_info["first-name"])
        self.driver.find_element(By.ID, "last-name").send_keys(checkout_info["last-name"])
        self.driver.find_element(By.ID, "postal-code").send_keys(checkout_info["postal-code"])
        self.driver.find_element(By.ID, "continue").click()

    def purchase(self):
        self.driver.find_element(By.ID, "finish").click()