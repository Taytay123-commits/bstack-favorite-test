import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from browserstack_config import capabilities, USERNAME, ACCESS_KEY, DEMO_PASS


@pytest.mark.parametrize("caps", capabilities)
def test_favorite_galaxy_s20(caps):
    browser_name = caps.get("browserName")

    # Define bstack:options (Selenium 4+ W3C format)
    bstack_options = {
        "userName": USERNAME,
        "accessKey": ACCESS_KEY,
        "buildName": "Galaxy Fav Build",
        "projectName": "Favorites Testing",
        "debug": "true"
    }

    # Attach bstack options
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
            # For mobile: use desired_capabilities directly
            driver = webdriver.Remote(
                command_executor="https://hub.browserstack.com/wd/hub",
                desired_capabilities=caps
            )

        driver.get("https://bstackdemo.com")

        wait = WebDriverWait(driver, 20)
        try:
            wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys("demouser")
            driver.find_element(By.ID, "password").send_keys(DEMO_PASS)
            driver.find_element(By.ID, "login-btn").click()
        except TimeoutException:
            print("DEBUG: Login elements not found.")
            print(driver.page_source)
            raise

        # Filter for Samsung devices
        wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Samsung']"))).click()

        # Favorite Galaxy S20+
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[text()='Galaxy S20+']/ancestor::div[contains(@class,'shelf-item')]//span[contains(@class,'favorite')]")
        )).click()

        # Go to Favorites
        wait.until(EC.element_to_be_clickable((By.ID, "favorites"))).click()

        # Confirm Galaxy S20+ is listed
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[text()='Galaxy S20+']")
        ))

    finally:
        if 'driver' in locals():
            driver.quit()
