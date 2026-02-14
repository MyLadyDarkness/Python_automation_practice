from src.pages.saucedemo.base_page import SauceBasePage
from src.pages.saucedemo.cart_page import CartPage
from src.pages.saucedemo.inventory_page import InventoryPage


def test_add_single_item(driver):
    login_page = SauceBasePage(driver)
    inventory_page = InventoryPage(driver)
    login_page.open()
    login_page.standard_login()
    inventory_page.add_cart()
    inventory_page.items_cart_quantity_assertions("1")

def test_add_multiple_items(driver):
    login_page = SauceBasePage(driver)
    inventory_page = InventoryPage(driver)
    login_page.open()
    login_page.standard_login()
    inventory_page.add_cart()
    inventory_page.add_cart()
    inventory_page.add_cart()
    inventory_page.items_cart_quantity_assertions("3")

def test_cart_item_details(driver):
    login_page = SauceBasePage(driver)
    inventory_page = InventoryPage(driver)

    login_page.open()
    login_page.standard_login()
    item_in_cart = inventory_page.add_cart()

    cart_page = inventory_page.go_to_cart()
    assert item_in_cart["name"] == cart_page.get_cart_item_details()[0]["name"]
    assert item_in_cart["price"] == cart_page.get_cart_item_details()[0]["price"]
    assert item_in_cart["description"] == cart_page.get_cart_item_details()[0]["description"]

def test_remove_item_from_cart(driver):
    login_page = SauceBasePage(driver)
    inventory_page = InventoryPage(driver)
    cart_page_item = CartPage(driver)

    login_page.open()
    login_page.standard_login()
    item_in_cart = inventory_page.add_cart()

    cart_page = inventory_page.go_to_cart()

    assert item_in_cart["name"] == cart_page.get_cart_item_details()[0]["name"]

    cart_page_item.remove_from_cart()

def test_remove_item_inventory(driver):
    login_page = SauceBasePage(driver)
    inventory_page = InventoryPage(driver)
    login_page.open()
    login_page.standard_login()
    inventory_page.add_cart()
    inventory_page.add_cart()
    inventory_page.items_cart_quantity_assertions("2")
    inventory_page.remove_item()
    inventory_page.items_cart_quantity_assertions("1")