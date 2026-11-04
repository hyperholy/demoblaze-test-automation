
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


# Selects a category and opens a product
def open_product(driver, category, product_name):
    category_link = WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable((By.XPATH, f"//a[@onclick=\"byCat('{category}')\"]"))
    )
    category_link.click()

    product = WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable((By.LINK_TEXT, product_name))
    )
    product.click()

    WebDriverWait(driver, WAIT_TIME).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#tbodyid h2"))
    )



# Verifies the product details
def verify_product_details(driver, expected_name):
    wait = WebDriverWait(driver, WAIT_TIME)

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#tbodyid h2")))

    name = driver.find_element(By.CSS_SELECTOR, "#tbodyid h2").text
    price = driver.find_element(By.CSS_SELECTOR, "#tbodyid h3.price-container").text
    description = driver.find_element(By.CSS_SELECTOR, "#more-information p").text
    image = driver.find_element(By.CSS_SELECTOR, "#imgp img")
    add_to_cart = driver.find_element(By.XPATH, "//a[contains(normalize-space(.), 'Add to cart')]")

    assert name == expected_name
    assert price != ""
    assert description != ""
    assert image.is_displayed()
    assert image.get_attribute("src") != ""
    assert add_to_cart.is_displayed()


# T004-A: View Phone Details
def test_phone_details(driver):
    open_homepage(driver)
    open_product(driver, "phone", "Samsung galaxy s6")

    verify_product_details(driver, "Samsung galaxy s6")
    driver.save_screenshot(str(SCREENSHOTS / "T004-A_phone_details.png"))


# T004-B: View Laptop Details
def test_laptop_details(driver):
    open_homepage(driver)
    open_product(driver, "notebook", "Sony vaio i5")

    verify_product_details(driver, "Sony vaio i5")
    driver.save_screenshot(str(SCREENSHOTS / "T004-B_laptop_details.png"))


# T004-C: View Monitor Details
def test_monitor_details(driver):
    open_homepage(driver)
    open_product(driver, "monitor", "Apple monitor 24")

    verify_product_details(driver, "Apple monitor 24")
    driver.save_screenshot(str(SCREENSHOTS / "T004-C_monitor_details.png"))

