
import uuid
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.demoblaze.com/index.html"
CART_URL = "https://www.demoblaze.com/cart.html"
WAIT_TIME = 30

SCREENSHOTS = Path("screenshots")
SCREENSHOTS.mkdir(exist_ok=True)


# Adds the Samsung galaxy s6 to the cart
def add_product(driver):
    wait = WebDriverWait(driver, WAIT_TIME)

    driver.get(BASE_URL)

    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@onclick=\"byCat('phone')\"]"))
    ).click()

    wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Samsung galaxy s6"))
    ).click()

    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Add to cart']"))
    ).click()

    alert = wait.until(EC.alert_is_present())
    assert "product added" in alert.text.lower()
    alert.accept()


# Opens the order form
def open_order_modal(driver):
    driver.get(CART_URL)

    wait = WebDriverWait(driver, WAIT_TIME)
    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Place Order']"))
    ).click()

    wait.until(EC.visibility_of_element_located((By.ID, "orderModal")))


# Fills the order form with unique details
def fill_order_form(driver, name=True, card=True):
    unique = uuid.uuid4().hex[:8]

    if name:
        driver.find_element(By.ID, "name").send_keys(f"Customer {unique}")

    driver.find_element(By.ID, "country").send_keys(f"Country {unique}")
    driver.find_element(By.ID, "city").send_keys(f"City {unique}")

    if card:
        driver.find_element(By.ID, "card").send_keys(f"12345678{unique}")

    driver.find_element(By.ID, "month").send_keys("November")
    driver.find_element(By.ID, "year").send_keys("2026")


# T006-A: Valid Order
def test_order_success(driver):
    add_product(driver)
    open_order_modal(driver)
    fill_order_form(driver)

    driver.find_element(By.XPATH, "//button[text()='Purchase']").click()

    wait = WebDriverWait(driver, WAIT_TIME)
    confirmation = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "sweet-alert"))
    )

    assert "thank you for your purchase" in confirmation.text.lower()

    driver.save_screenshot(str(SCREENSHOTS / "T006-A_success.png"))


# T006-B: Missing Name
def test_order_missing_name(driver):
    add_product(driver)
    open_order_modal(driver)
    fill_order_form(driver, name=False)

    driver.find_element(By.XPATH, "//button[text()='Purchase']").click()

    wait = WebDriverWait(driver, WAIT_TIME)
    alert = wait.until(EC.alert_is_present())

    assert "please fill out name and creditcard" in alert.text.lower()

    alert.accept()
    driver.save_screenshot(str(SCREENSHOTS / "T006-B_missing_name.png"))


# T006-C: Missing Credit Card
def test_order_missing_card(driver):
    add_product(driver)
    open_order_modal(driver)
    fill_order_form(driver, card=False)

    driver.find_element(By.XPATH, "//button[text()='Purchase']").click()

    wait = WebDriverWait(driver, WAIT_TIME)
    alert = wait.until(EC.alert_is_present())

    assert "please fill out name and creditcard" in alert.text.lower()

    alert.accept()
    driver.save_screenshot(str(SCREENSHOTS / "T006-C_missing_card.png"))
