import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from browserstack_config import USERNAME, ACCESS_KEY, capabilities, DEMO_USER, DEMO_PASS

DEMO_USER = os.environ.get("DEMO_USER")
DEMO_PASS = os.environ.get("DEMO_PASS")

@pytest.mark.parametrize("caps", capabilities)
def test_favorite_galaxy_s20(caps):
    browser_name = caps.get("browserName")

    bstack_options = {
        "userName": USERNAME,
        "accessKey": ACCESS_KEY,
        "buildName": "Galaxy Fav Build",
        "projectName": "Favorites Testing",
        "debug": "true"
    }

    caps["bstack:options"] = bstack_options

    try:
        if browser_name in ["Chrome", "Firefox"]:
            if browser_name == "Chrome":
                options = webdriver.ChromeOptions()
            else:
                options = webdriver.FirefoxOptions()

            for key, value in caps.items():
                options.set_capability(key, value)

            driver = webdriver.Remote(
                command_executor="https://hub.browserstack.com/wd/hub",
                options=options
            )
        else:
            mobile_options = webdriver.ChromeOptions()
            for key, value in caps.items():
                mobile_options.set_capability(key, value)
            driver = webdriver.Remote(
                command_executor="https://hub.browserstack.com/wd/hub",
                options=mobile_options
            )

        driver.get("https://bstackdemo.com")
        wait = WebDriverWait(driver, 20)

        # Click Sign In to open the login form
        wait.until(EC.element_to_be_clickable((By.ID, "signin"))).click()

        # Locate username container then find input inside and send keys
        username_container = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_input = username_container.find_element(By.TAG_NAME, "input")
        username_input.send_keys(DEMO_USER)
        username_input.send_keys(Keys.ENTER)

        # Locate password container then find input inside and send keys
        password_container = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_input = password_container.find_element(By.TAG_NAME, "input")
        password_input.send_keys(DEMO_PASS)
        password_input.send_keys(Keys.ENTER)

        # Wait for login to complete by checking cart or welcome
        wait.until(EC.presence_of_element_located((By.ID, "logout")))

        # Filter by Samsung
        wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Samsung']"))).click()

        # Favorite Galaxy S20+
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[text()='Galaxy S20+']/ancestor::div[contains(@class, 'shelf-item')]//span[@class='favorite']"))
        ).click()

        # Go to Favorites
        wait.until(EC.element_to_be_clickable((By.ID, "favorites"))).click()

        # Check Galaxy S20+ is in the list
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Galaxy S20+']")))

    finally:
        driver.quit()
