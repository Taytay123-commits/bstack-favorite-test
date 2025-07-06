import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("DEMO_USERNAME")
PASSWORD = os.getenv("DEMO_PASSWORD")
BROWSERSTACK_USERNAME = os.getenv("BROWSERSTACK_USERNAME")
BROWSERSTACK_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")

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
        "osVersion": "Monterey"
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
        "userName": BROWSERSTACK_USERNAME,
        "accessKey": BROWSERSTACK_ACCESS_KEY,
        "buildName": "Galaxy Fav Build",
        "projectName": "Favorites Testing",
        "debug": "true"
    }

    caps["bstack:options"] = bstack_options

    options = webdriver.ChromeOptions()
    for key, value in caps.items():
        options.set_capability(key, value)

    driver = webdriver.Remote(
        command_executor="https://hub.browserstack.com/wd/hub",
        options=options
    )

    wait = WebDriverWait(driver, 20)
    driver.get("https://bstackdemo.com")

    # Login
    wait.until(EC.element_to_be_clickable((By.ID, "signin"))).click()

    username_input = wait.until(EC.presence_of_element_located((By.ID, "username"))).find_element(By.TAG_NAME, "input")
    username_input.send_keys(USERNAME)
    username_input.send_keys(Keys.ENTER)

    password_input = wait.until(EC.presence_of_element_located((By.ID, "password"))).find_element(By.TAG_NAME, "input")
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.ENTER)

    wait.until(EC.element_to_be_clickable((By.ID, "login-btn"))).click()
    wait.until(lambda d: "signin=true" in d.current_url)
    assert "signin=true" in driver.current_url

    # Click Samsung checkbox
    samsung_checkbox_label = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//label[input[@value='Samsung']]"))
    )
    samsung_checkbox_label.click()

    # Click Favorite on Galaxy S20+
    favorite_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-sku='samsung-S20+-device-info.png'] button[aria-label='delete']"))
    )
    favorite_btn.click()

    # Navigate to Favourites
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a#favourites"))).click()

    # Check Galaxy S20+ is in favourites
    fav_item = wait.until(
        EC.presence_of_element_located((By.XPATH, "//p[contains(@class, 'shelf-item__title') and text()='Galaxy S20+']"))
    )
    assert fav_item.is_displayed()

    driver.quit()
