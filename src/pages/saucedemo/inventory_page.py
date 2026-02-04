import random
from selenium.webdriver.common.by import By
from src.pages.saucedemo.base_page import SauceBasePage

class InventoryPage(SauceBasePage):

    def add_cart(self):
        all_items = self.driver.find_elements(By.CSS_SELECTOR, "[class*=btn_inventory][name*=add]")

        if all_items:
            random_item = random.choice(all_items)
            random_item.click()

        else:
            print("Nothing add to cart")