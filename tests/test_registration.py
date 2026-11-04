
import uuid
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.demoblaze.com/index.html"
USERNAME = f"test_{uuid.uuid4().hex[:10]}"
PASSWORD = "TestPassword123"

SCREENSHOTS = Path("screenshots")
SCREENSHOTS.mkdir(exist_ok=True)


# Opens the signup modal
def open_signup(driver):
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)

    wait.until(EC.element_to_be_clickable((By.ID, "signin2"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, "sign-username")))


# Submit the signup form with arguments
def submit_signup(driver, username, password):
    driver.find_element(By.ID, "sign-username").send_keys(username)
    driver.find_element(By.ID, "sign-password").send_keys(password)
    driver.find_element(By.XPATH, "//button[text()='Sign up']").click()


# Wait for and return the current JavaScript alert
def read_alert(driver):
    alert = WebDriverWait(driver, 30).until(EC.alert_is_present())
    return alert.text, alert


# T001-A: Valid Registration
def test_registration_success(driver):
    open_signup(driver)
    submit_signup(driver, USERNAME, PASSWORD)

    message, alert = read_alert(driver)
    assert "sign up successful" in message.lower()

    alert.accept()
    driver.save_screenshot(str(SCREENSHOTS / "T001-A_success.png"))


# T001-B: Duplicate Registration
def test_registration_duplicate(driver):
    username = f"duplicate_{uuid.uuid4().hex[:10]}"

    open_signup(driver)
    submit_signup(driver, username, PASSWORD)

    message, alert = read_alert(driver)
    assert "sign up successful" in message.lower()
    alert.accept()

    open_signup(driver)
    submit_signup(driver, username, PASSWORD)

    message, alert = read_alert(driver)
    assert "already exist" in message.lower()

    alert.accept()
    driver.save_screenshot(str(SCREENSHOTS / "T001-B_duplicate.png"))


# T001-C: Empty Credentials
def test_registration_empty(driver):
    open_signup(driver)
    submit_signup(driver, "", "")

    message, alert = read_alert(driver)
    assert "please fill out username and password" in message.lower()

    alert.accept()
    driver.save_screenshot(str(SCREENSHOTS / "T001-C_empty.png"))