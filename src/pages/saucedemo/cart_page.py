from selenium.webdriver.common.by import By
from src.pages.saucedemo.base_page import SauceBasePage
from selenium.common.exceptions import NoSuchElementException
import pytest

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
            self.find((By.CSS_SELECTOR, "class*=checkout_button")).click()

        else:
            raise Exception("Cannot checkout: cart is empty")

    # def purchase(self):
    #     # cart_items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
    #     # if cart_items:
    #     #     self.find((By.CSS_SELECTOR, "class*=checkout_button")).click()
    #         assert self.find((By.CLASS_NAME, "title")).text == "Checkout: Your Information"
    #
    #         self.find((By.CSS_SELECTOR, "placeholder=First Name")).send_keys("Test First")
    #         self.find((By.CSS_SELECTOR, "placeholder=Last Name")).send_keys("Test Last")
    #         self.find((By.CSS_SELECTOR, "placeholder=Zip/Postal Code")).send_keys("299045")
    #
    #         self.find((By.ID, "continue")).click()
    #
    #         assert self.find((By.CLASS_NAME, "title")).text == "Checkout: Your Information"
    #         self.find((By.ID, "finish")).click()

