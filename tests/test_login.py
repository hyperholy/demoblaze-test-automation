
import uuid
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.demoblaze.com/index.html"
PASSWORD = "TestPassword123"
WAIT_TIME = 30

SCREENSHOTS = Path("screenshots")
SCREENSHOTS.mkdir(exist_ok=True)


# Opens the login modal
def open_login(driver):
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, WAIT_TIME)

    wait.until(EC.element_to_be_clickable((By.ID, "login2"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, "loginusername")))


# Creates a registered account for login testing
def create_test_account(driver):
    username = f"login_{uuid.uuid4().hex[:10]}"

    driver.get(BASE_URL)
    wait = WebDriverWait(driver, WAIT_TIME)

    wait.until(EC.element_to_be_clickable((By.ID, "signin2"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, "sign-username")))

    driver.find_element(By.ID, "sign-username").send_keys(username)
    driver.find_element(By.ID, "sign-password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[text()='Sign up']").click()

    alert = wait.until(EC.alert_is_present())
    assert "sign up successful" in alert.text.lower()
    alert.accept()

    return username


# Submits the login form with arguments
def submit_login(driver, username, password):
    driver.find_element(By.ID, "loginusername").send_keys(username)
    driver.find_element(By.ID, "loginpassword").send_keys(password)
    driver.find_element(By.XPATH, "//button[text()='Log in']").click()


# Wait for and return the current JavaScript alert
def read_alert(driver):
    alert = WebDriverWait(driver, WAIT_TIME).until(EC.alert_is_present())
    return alert.text, alert


# T002-A: Valid Login
def test_login_success(driver):
    username = create_test_account(driver)

    open_login(driver)
    submit_login(driver, username, PASSWORD)

    welcome = WebDriverWait(driver, WAIT_TIME).until(
        EC.visibility_of_element_located((By.ID, "nameofuser"))
    )

    assert username in welcome.text
    driver.save_screenshot(str(SCREENSHOTS / "T002-A_success.png"))


# T002-B: Invalid Password
def test_login_invalid_password(driver):
    username = create_test_account(driver)

    open_login(driver)
    submit_login(driver, username, "IncorrectPassword123")

    message, alert = read_alert(driver)
    assert "wrong password" in message.lower()

    alert.accept()
    driver.save_screenshot(str(SCREENSHOTS / "T002-B_invalid_password.png"))


# T002-C: Empty Credentials
def test_login_empty(driver):
    open_login(driver)
    submit_login(driver, "", "")

    message, alert = read_alert(driver)
    assert "please fill out username and password" in message.lower()

    alert.accept()
    driver.save_screenshot(str(SCREENSHOTS / "T002-C_empty.png"))
