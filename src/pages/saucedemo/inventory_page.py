import random
from selenium.webdriver.common.by import By
from src.pages.saucedemo.base_page import SauceBasePage

class InventoryPage(SauceBasePage):

    def add_cart(self):
        all_items_buttons = self.driver.find_elements(By.CSS_SELECTOR, "[class*=btn_inventory][name*=add]")
        all_items_names = self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        all_items_prices = self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        all_tems_descr = self.driver.find_elements(By.CLASS_NAME, "inventory_item_desc")

        if not all_items_buttons:
            print("Nothing add to cart")

        random_item_index = random.randint(0, len(all_items_buttons) - 1)

        item_name =  all_items_names[random_item_index].text
        item_price = all_items_prices[random_item_index].text
        item_descr = all_tems_descr[random_item_index].text

        all_items_buttons[random_item_index].click()

        return {
            "name": item_name,
            "price": item_price,
            "descr": item_descr,
            "index": random_item_index  # Индекс для отладки
        }

    def remove_item(self):
        all_items = self.driver.find_elements(By.CSS_SELECTOR, "[class*=btn_inventory][name*=remove]")

        if all_items:
            random_item = random.choice(all_items)
            random_item.click()

        else:
            print("Nothing to remove")

    def items_cart_quantity(self, quantity):
        assert self.find((By.CSS_SELECTOR, "[class=shopping_cart_badge]")).text == quantity

