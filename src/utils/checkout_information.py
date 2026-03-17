from selenium.webdriver.common.by import By
from src.utils.unique_id_gen import generated_unique_id

def checkout_information():
    # first_name = self.driver.find_element(By.ID, "first-name")
    # first_name.send_keys(f"first_name_{generated_unique_id()}")
    #
    # last_name = self.driver.find_element(By.ID, "last-name")
    # last_name.send_keys(f"last_name_{generated_unique_id()}")
    #
    # zip_code = self.driver.find_element(By.ID, "postal-code")
    # zip_code.send_keys(f"postal_code_{generated_unique_id()}")
    #
    # self.driver.find_element(By.ID, "continue").click()
    # self.driver.find_element(By.ID, "finish").click()

    first_name = f"first_name_{generated_unique_id()}"
    last_name = f"last_name_{generated_unique_id()}"
    postal_code = f"postal_code_{generated_unique_id()}"

    return {
        "first-name" : first_name,
        "last-name" : last_name,
        "postal-code" : postal_code
    }