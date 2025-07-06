import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browserstack_config import capabilities, USERNAME, ACCESS_KEY, DEMO_PASS

@pytest.mark.parametrize("caps", capabilities)
def test_favorite_galaxy_s20(caps):
    caps["browserstack.user"] = USERNAME
    caps["browserstack.key"] = ACCESS_KEY
    caps["build"] = "Galaxy Fav Build"
    caps["project"] = "Favorites Testing"
    caps["browserstack.debug"] = "true"

    browser_name = caps.get("browserName")

    # Choose the appropriate options object for browser
    options = None
    if browser_name == "Chrome":
        options = webdriver.ChromeOptions()
    elif browser_name == "Firefox":
        options = webdriver.FirefoxOptions()

    if options:
        for key, value in caps.items():
            options.set_capability(key, value)

        driver = webdriver.Remote(
            command_executor="http://hub.browserstack.com/wd/hub",
            options=options
        )
    else:
        # For mobile caps, pass caps directly (no options)
        driver = webdriver.Remote(
            command_executor="http://hub.browserstack.com/wd/hub",
            options=None
        )
        driver.capabilities.update(caps)

    driver.get("https://bstackdemo.com")
    wait = WebDriverWait(driver, 10)

    wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys("demouser")
    driver.find_element(By.ID, "password").send_keys(DEMO_PASS)
    driver.find_element(By.ID, "login-btn").click()

    # Filter to Samsung
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Samsung']"))).click()

    # Favorite Galaxy S20+
    wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Samsung Galaxy S20+']/following-sibling::div//span[@class='wishlist']"))).click()

    # Navigate to Favorites
    driver.find_element(By.ID, "favorites").click()

    # Validate Galaxy S20+ appears
    wait.until(EC.visibility_of_element_located((By.XPATH, "//p[text()='Samsung Galaxy S20+']")))

    driver.quit()
