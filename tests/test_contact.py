
import uuid
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.demoblaze.com/index.html"
WAIT_TIME = 30

SCREENSHOTS = Path("screenshots")
SCREENSHOTS.mkdir(exist_ok=True)


# Opens the contact modal
def open_contact(driver):
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, WAIT_TIME)

    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Contact']"))
    ).click()

    wait.until(
        EC.visibility_of_element_located((By.ID, "exampleModal"))
    )


# Fills the contact form
def fill_contact_form(driver, email=True, message=True):
    unique = uuid.uuid4().hex[:8]

    if email:
        driver.find_element(By.ID, "recipient-email").send_keys(
            f"test_{unique}@example.com"
        )

    driver.find_element(By.ID, "recipient-name").send_keys(
        f"Tester {unique}"
    )

    if message:
        driver.find_element(By.ID, "message-text").send_keys(
            f"Automated test message {unique}"
        )


# Submits the contact form
def send_message(driver):
    driver.find_element(
        By.XPATH, "//button[normalize-space()='Send message']"
    ).click()


# Waits for and returns the JavaScript alert
def read_alert(driver):
    alert = WebDriverWait(driver, WAIT_TIME).until(
        EC.alert_is_present()
    )
    return alert.text, alert


# T007-A: Valid Contact Message
def test_contact_success(driver):
    open_contact(driver)
    fill_contact_form(driver)

    send_message(driver)

    message, alert = read_alert(driver)

    alert.accept()
    driver.save_screenshot(str(SCREENSHOTS / "T007-A_success.png"))
    assert "thanks for the message" in message.lower()


# T007-B: Missing Email
def test_contact_missing_email(driver):
    open_contact(driver)
    fill_contact_form(driver, email=False)

    send_message(driver)

    message, alert = read_alert(driver)

    alert.accept()
    driver.save_screenshot(str(SCREENSHOTS / "T007-B_missing_email.png"))
    assert "fill out" in message.lower()


# T007-C: Missing Message
def test_contact_missing_message(driver):
    open_contact(driver)
    fill_contact_form(driver, message=False)

    send_message(driver)

    message, alert = read_alert(driver)

    alert.accept()
    driver.save_screenshot(str(SCREENSHOTS / "T007-C_missing_message.png"))
    assert "fill out" in message.lower()
