import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from browserstack_config import USERNAME, ACCESS_KEY, capabilities, DEMO_USERNAME, DEMO_PASSWORD

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
        # Choose options based on device or desktop
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

        wait = WebDriverWait(driver, 20)
        driver.get("https://bstackdemo.com")

        # Click Sign In to open the login modal
        wait.until(EC.element_to_be_clickable((By.ID, "signin"))).click()

        # Enter username
        username_container = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_input = username_container.find_element(By.TAG_NAME, "input")
        username_input.send_keys(DEMO_USERNAME)
        username_input.send_keys(Keys.ENTER)

        # Enter password
        password_container = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_input = password_container.find_element(By.TAG_NAME, "input")
        password_input.send_keys(DEMO_PASSWORD)
        password_input.send_keys(Keys.ENTER)

        # Click login button
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "login-btn")))
        login_button.click()

        # ✅ Confirm login was successful by checking URL contains login=true
        wait.until(lambda d: "signin=true" in d.current_url)
        assert "signin=true" in driver.current_url

        # Filter by Samsung
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='samsung']"))).click()

        # Favorite the Galaxy S20+
        favorite_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//p[text()='Galaxy S20+']/../..//span[@class='favorite']"))
        )
        favorite_button.click()

        # Navigate to Favorites
        wait.until(EC.element_to_be_clickable((By.ID, "favorites"))).click()

        # Assert Galaxy S20+ is present in Favorites
        wait.until(EC.presence_of_element_located((By.XPATH, "//p[text()='Galaxy S20+']")))

    finally:
        driver.quit()

