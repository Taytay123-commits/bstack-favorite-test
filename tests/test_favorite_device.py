import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USERNAME = os.getenv("BROWSERSTACK_USERNAME")
ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")
DEMO_USERNAME = os.getenv("DEMO_USERNAME")
DEMO_PASSWORD = os.getenv("DEMO_PASSWORD")

capabilities = [
    {
        "browserName": "Chrome",
        "browserVersion": "latest",
        "os": "Windows",
        "osVersion": "10",
    },
    {
        "browserName": "Firefox",
        "browserVersion": "latest",
        "os": "OS X",
        "osVersion": "Ventura",
    },
    {
        "deviceName": "Samsung Galaxy S22",
        "realMobile": "true",
        "osVersion": "12.0",
    },
]

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
        # Select appropriate driver
        if browser_name in ["Chrome", "Firefox"]:
            options = webdriver.ChromeOptions() if browser_name == "Chrome" else webdriver.FirefoxOptions()
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

        # Click Sign In
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

        # Confirm login by URL
        wait.until(lambda d: "signin=true" in d.current_url)
        assert "signin=true" in driver.current_url

        # Click the Samsung checkbox
        samsung_checkbox_label = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//label[.//span[text()='Samsung']]"))
        )
        samsung_checkbox_label.click()

        # Click the heart icon to favorite the Galaxy S20+
        fav_button = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//p[text()='Galaxy S20+']/ancestor::div[contains(@class, 'shelf-item')]//button[@aria-label='delete']"
        )))
        fav_button.click()

        # Go to Favourites
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a#favourites"))).click()

        # Confirm Galaxy S20+ is in favourites
        fav_s20 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.shelf-item[data-sku='samsung-S20+-device-info.png']"))
        )
        assert fav_s20.is_displayed()

    finally:
        driver.quit()

