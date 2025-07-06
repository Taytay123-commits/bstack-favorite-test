import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USERNAME = os.environ.get("BROWSERSTACK_USERNAME")
ACCESS_KEY = os.environ.get("BROWSERSTACK_ACCESS_KEY")

capabilities = [
    {
        "browserName": "Chrome",
        "browserVersion": "latest",
        "os": "Windows",
        "osVersion": "10"
    },
    {
        "browserName": "Firefox",
        "browserVersion": "latest",
        "os": "OS X",
        "osVersion": "Ventura"
    },
    {
        "deviceName": "Samsung Galaxy S22",
        "realMobile": "true",
        "osVersion": "12.0"
    }
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

        # Sign In
        sign_in = wait.until(EC.element_to_be_clickable((By.ID, "signin")))
        sign_in.click()

        # Username dropdown
        username_container = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_input = username_container.find_element(By.TAG_NAME, "input")
        username_input.click()
        username_input.send_keys("bstack-demo-username")
        username_input.send_keys(Keys.ENTER)

        # Password dropdown
        password_container = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_input = password_container.find_element(By.TAG_NAME, "input")
        password_input.click()
        password_input.send_keys("bstack-demo-password")
        password_input.send_keys(Keys.ENTER)

        # Submit login
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "login-btn")))
        login_button.click()

        # Filter for Samsung only
        samsung_filter = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Samsung']")))
        samsung_filter.click()

        # Favorite Galaxy S20+
        favorite_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Galaxy S20+']/../../..//span[@class='checkmark']")))
        favorite_icon.click()

        # Go to Favorites
        favorites_link = wait.until(EC.element_to_be_clickable((By.ID, "favorites")))
        favorites_link.click()

        # Verify Galaxy S20+ is listed
        wait.until(EC.

