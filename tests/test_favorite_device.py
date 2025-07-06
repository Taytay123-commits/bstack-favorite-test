import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browserstack_config import capabilities, USERNAME, ACCESS_KEY, DEMO_PASS


@pytest.mark.parametrize("caps", capabilities)
def test_favorite_galaxy_s20(caps):
    browser_name = caps.get("browserName")

    # Attach bstack options
    bstack_options = {
        "userName": USERNAME,
        "accessKey": ACCESS_KEY,
        "buildName": "Galaxy Fav Build",
        "projectName": "Favorites Testing",
        "debug": "true"
    }
    caps["bstack:options"] = bstack_options

    try:
        # Setup driver
        if browser_name in ["Chrome", "Firefox"]:
            options = webdriver.ChromeOptions() if browser_name == "Chrome" else webdriver.FirefoxOptions()
            for key, value in caps.items():
                options.set_capability(key, value)
            driver = webdriver.Remote("https://hub.browserstack.com/wd/hub", options=options)
        else:
            mobile_options = webdriver.ChromeOptions()
            for key, value in caps.items():
                mobile_options.set_capability(key, value)
            driver = webdriver.Remote("https://hub.browserstack.com/wd/hub", options=mobile_options)

        wait = WebDriverWait(driver, 20)
        driver.get("https://bstackdemo.com")

        # Click "Sign In" in the top right
        sign_in_btn = wait.until(EC.element_to_be_clickable((By.ID, "signin")))
        sign_in_btn.click()

        # Fill in Username (inside container with ID 'username')
        username_container = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_input = username_container.find_element(By.TAG_NAME, "input")
        username_input.send_keys("demouser")

        # Fill in Password (inside container with ID 'password')
        password_container = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_input = password_container.find_element(By.TAG_NAME, "input")
        password_input.send_keys(DEMO_PASS)

        # Submit Login
        login_btn = wait.until(EC.element_to_be_clickable((By.ID, "login-btn")))
        login_btn.click()

        # Filter for Samsung
        samsung_filter = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Samsung']")))
        samsung_filter.click()

        # Favorite the Galaxy S20+
        favorite_icon = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//p[text()='Galaxy S20+']/ancestor::div[@class='shelf-item']//span[contains(@class, 'bn-heart')]"
        )))
        favorite_icon.click()

        # Go to favorites
        favorites_btn = wait.until(EC.element_to_be_clickable((By.ID, "favorites")))
        favorites_btn.click()

        # Confirm favorite exists
        wait.until(EC.presence_of_element_located((By.XPATH, "//p[text()='Galaxy S20+']")))

    finally:
        driver.quit()
