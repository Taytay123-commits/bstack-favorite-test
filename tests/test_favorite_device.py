import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from browserstack_config import capabilities, USERNAME, ACCESS_KEY, DEMO_PASS


@pytest.mark.parametrize("caps", capabilities)
def test_favorite_galaxy_s20(caps):
    # Attach BrowserStack credentials using bstack:options
    bstack_options = {
        "userName": USERNAME,
        "accessKey": ACCESS_KEY,
        "buildName": "Galaxy Fav Build",
        "projectName": "Favorites Testing",
        "debug": "true",
        "seleniumVersion": "4.8.0"
    }
    caps["bstack:options"] = {**caps.get("bstack:options", {}), **bstack_options}

    browser_name = caps.get("browserName")

    try:
        # Set capabilities using browser-specific options
        if browser_name == "Chrome":
            options = webdriver.ChromeOptions()
        elif browser_name == "Firefox":
            options = webdriver.FirefoxOptions()
        elif caps.get("deviceName"):  # Mobile
            options = webdriver.ChromeOptions()  # or leave blank
        else:
            raise Exception("Unsupported browser/device config.")

        for key, value in caps.items():
            options.set_capability(key, value)

        driver = webdriver.Remote(
            command_executor="https://hub.browserstack.com/wd/hub",
            options=options
        )

        driver.get("https://bstackdemo.com")
        wait = WebDriverWait(driver, 20)

        # Log in
        try:
            wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys("demouser")
            driver.find_element(By.ID, "password").send_keys(DEMO_PASS)
            driver.find_element(By.ID, "login-btn").click()
        except TimeoutException:
            print("Login fields not found — layout might differ on mobile.")
            print(driver.page_source)
            raise

        # Filter to Samsung devices
        wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Samsung']"))).click()

        # Favorite Galaxy S20+
        wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//div[text()='Galaxy S20+']/ancestor::div[contains(@class,'shelf-item')]//span[contains(@class,'favorite')]"
        ))).click()

        # Go to favorites
        wait.until(EC.element_to_be_clickable((By.ID, "favorites"))).click()

        # Verify it's listed
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[text()='Galaxy S20+']")
        ))

    finally:
        if 'driver' in locals():
            driver.quit()
