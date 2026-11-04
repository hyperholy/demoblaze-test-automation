
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.demoblaze.com/index.html"
WAIT_TIME = 30

SCREENSHOTS = Path("screenshots")
SCREENSHOTS.mkdir(exist_ok=True)


# Adds a product to the cart
def add_product(driver, category, product_name):
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, WAIT_TIME)

    category_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//a[@onclick=\"byCat('{category}')\"]"))
    )
    category_link.click()

    product = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, product_name))
    )
    product.click()

    wait.until(
        EC.visibility_of_element_located((By.XPATH, "//a[text()='Add to cart']"))
    ).click()

    alert = wait.until(EC.alert_is_present())
    assert "product added" in alert.text.lower()
    alert.accept()


# Opens the shopping cart
def open_cart(driver):
    wait = WebDriverWait(driver, WAIT_TIME)

    wait.until(EC.element_to_be_clickable((By.ID, "cartur"))).click()

    wait.until(EC.presence_of_element_located((By.ID, "tbodyid")))


# Retrieves the products currently in the cart
def get_cart_products(driver):
    rows = driver.find_elements(By.CSS_SELECTOR, "#tbodyid tr")

    return [
        {
            "name": row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text,
            "price": row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
        }
        for row in rows
    ]


# T005-A: Add Product to Cart
def test_add_product(driver):
    add_product(driver, "phone", "Samsung galaxy s6")
    open_cart(driver)

    wait = WebDriverWait(driver, WAIT_TIME)
    wait.until(
        lambda d: any(
            row["name"] == "Samsung galaxy s6"
            for row in get_cart_products(d)
        )
    )

    products = get_cart_products(driver)

    assert any(
        product["name"] == "Samsung galaxy s6" and product["price"] != ""
        for product in products
    )

    driver.save_screenshot(str(SCREENSHOTS / "T005-A_add_product.png"))


# T005-B: Delete Product from Cart
def test_delete_product(driver):
    add_product(driver, "phone", "Samsung galaxy s6")
    open_cart(driver)

    wait = WebDriverWait(driver, WAIT_TIME)
    wait.until(lambda d: len(get_cart_products(d)) > 0)

    delete = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Delete"))
    )
    delete.click()

    wait.until(lambda d: len(get_cart_products(d)) == 0)

    assert len(get_cart_products(driver)) == 0
    driver.save_screenshot(str(SCREENSHOTS / "T005-B_delete_product.png"))


# T005-C: Add Multiple Products
def test_add_multiple_products(driver):
    add_product(driver, "phone", "Samsung galaxy s6")
    add_product(driver, "phone", "Nokia lumia 1520")

    open_cart(driver)

    wait = WebDriverWait(driver, WAIT_TIME)
    wait.until(lambda d: len(get_cart_products(d)) >= 2)

    products = get_cart_products(driver)
    names = [product["name"] for product in products]

    assert "Samsung galaxy s6" in names
    assert "Nokia lumia 1520" in names
    assert all(product["price"] != "" for product in products)

    driver.save_screenshot(str(SCREENSHOTS / "T005-C_multiple_products.png"))
