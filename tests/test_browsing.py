
import time
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.demoblaze.com/index.html"
WAIT_TIME = 30

SCREENSHOTS = Path("screenshots")
SCREENSHOTS.mkdir(exist_ok=True)


# Opens the homepage
def open_homepage(driver):
    driver.get(BASE_URL)
    WebDriverWait(driver, WAIT_TIME).until(
        EC.visibility_of_element_located((By.ID, "tbodyid"))
    )


# Selects a product category and waits for products to load
def select_category(driver, category):
    link = WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable((By.XPATH, f"//a[@onclick=\"byCat('{category}')\"]"))
    )
    link.click()

    WebDriverWait(driver, WAIT_TIME).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "#tbodyid .card-title a")) > 0
    )


# Retrieves the displayed product names
def get_products(driver):
    return [
        product.text
        for product in driver.find_elements(By.CSS_SELECTOR, "#tbodyid .card-title a")
    ]


# T003-A: Browse Phones
def test_browse_phones(driver):
    open_homepage(driver)
    select_category(driver, "phone")
    # Unconditionaly wait, without including additional libraries
    time.sleep(WAIT_TIME)

    products = get_products(driver)

    assert products[0] == "Samsung galaxy s6"
    driver.save_screenshot(str(SCREENSHOTS / "T003-A_phones.png"))


# T003-B: Browse Laptops
def test_browse_laptops(driver):
    open_homepage(driver)
    select_category(driver, "notebook")
    time.sleep(WAIT_TIME)
    
    products = get_products(driver)

    assert products[0] == "Sony vaio i5"
    driver.save_screenshot(str(SCREENSHOTS / "T003-B_laptops.png"))


# T003-C: Browse Monitors
def test_browse_monitors(driver):
    open_homepage(driver)
    select_category(driver, "monitor")
    time.sleep(WAIT_TIME)

    products = get_products(driver)

    assert products[0] == "Apple monitor 24"
    driver.save_screenshot(str(SCREENSHOTS / "T003-C_monitors.png"))
