import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browserstack_config import capabilities, USERNAME, ACCESS_KEY, DEMO_PASS


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
            options = (
                webdriver.ChromeOptions()
                if browser_name == "Chrome"
                else webdriver.FirefoxOptions()
            )
            for key, value in caps.items():
                options.set_capability(key, value)

            driver = webdriver.Remote(
                command_executor="https://hub.browserstack.com/wd/hub",
                options=options,
            )
        else:
            mobile_options = webdriver.ChromeOptions()
            for key, value in caps.items():
                mobile_options.set_capability(key, value)

            driver = webdriver.Remote(
                command_executor="https://hub.browserstack.com/wd/hub",
                options=mobile_options,
            )

        driver.get("https://bstackdemo.com")
        wait = WebDriverWait(driver, 20)

        # Click "Sign In"
        wait.until(EC.element_to_be_clickable((By.ID, "signin"))).click()

        # === Username Dropdown ===
        wait.until(EC.element_to_be_clickable((By.ID, "username")))
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#username div[class$='-indicator']"))
        ).click()
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@id='username']//div[text()='demouser']"))
        ).click()

        # === Password Dropdown ===
        wait.until(EC.element_to_be_clickable((By.ID, "password")))
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#password div[class$='-indicator']"))
        ).click()
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//div[@id='password']//div[text()='{DEMO_PASS}']"))
        ).click()

        # Click Login button
        wait.until(EC.element_to_be_clickable((By.ID, "login-btn"))).click()

        # Filter for Samsung
        wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Samsung']"))).click()

        # Favorite Galaxy S20+
        wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//p[text()='Galaxy S20+']/ancestor::div[@class='shelf-item']//span[contains(@class, 'bn-heart')]"
        ))).click()

        # Go to favorites page
        wait.until(EC.element_to_be_clickable((By.ID, "favorites"))).click()

        # Confirm Galaxy S20+ is in favorites
        wait.until(EC.presence_of_element_located((By.XPATH, "//p[text()='Galaxy S20+']")))

    finally:
        driver.quit()

