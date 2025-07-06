import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load credentials from environment variables
USERNAME = os.getenv("BROWSERSTACK_USERNAME")
ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")
DEMO_USER = os.getenv("DEMO_USER")
DEMO_PASS = os.getenv("DEMO_PASS")

# Capabilities for parallel runs
capabilities = [
    {
        "os": "Windows",
        "osVersion": "10",
        "browserName": "Chrome",
        "browserVersion": "latest",
        "name": "Windows Chrome Test"
    },
    {
        "os": "OS X",
        "osVersion": "Ventura",
        "browserName": "Firefox",
        "browserVersion": "latest",
        "name": "macOS Firefox Test"
    },
    {
        "deviceName": "Samsung Galaxy S22",
        "realMobile": "true",
        "platformName": "Android",
        "name": "Samsung Galaxy S22 Test"
    }
]

@pytest.mark.parametrize("caps", capabilities)
def test_favorite_galaxy_s20(caps):
    # Inject BrowserStack credentials
    caps["browserstack.user"] = USERNAME
    caps["browserstack.key"] = ACCESS_KEY
    caps["build"] = "Galaxy Fav Build"
    caps["project"] = "Favorites Testing"
    caps["browserstack.debug"] = "true"

    driver = webdriver.Remote(
        command_executor="http://hub.browserstack.com/wd/hub",
        options=webdriver.ChromeOptions() if caps.get("browserName") == "Chrome" else None,
        desired_capabilities=caps
    )

    wait = WebDriverWait(driver, 10)
    try:
        # Open demo site
        driver.get("https://www.bstackdemo.com/")

        # Log in
        wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys(DEMO_USER)
        driver.find_element(By.ID, "password").send_keys(DEMO_PASS)
        driver.find_element(By.ID, "login-btn").click()

        # Filter to Samsung only
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Samsung']"))).click()

        # Wait for filtered products to show
        wait.until(EC.presence_of_element_located((By.XPATH, "//p[text()='Samsung Galaxy S20+']")))

        # Click the yellow heart icon to favorite
        heart_icon = driver.find_element(By.XPATH, "//p[text()='Samsung Galaxy S20+']/../..//span[contains(@class, 'favorite')]")
        heart_icon.click()

        # Navigate to Favorites page
        driver.find_element(By.ID, "favorites").click()

        # Verify Galaxy S20+ is listed
        wait.until(EC.visibility_of_element_located((By.XPATH, "//p[text()='Samsung Galaxy S20+']")))

    finally:
        driver.quit()

