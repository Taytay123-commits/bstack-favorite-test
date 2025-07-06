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

        # Click "Sign In" in the top right
        wait.until(EC.element_to_be_clickable((By.ID, "signin"))).click()

        # Enter credentials using the correct <input> fields
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#username input"))).send_keys("demouser")
        driver.find_element(By.CSS_SELECTOR, "#password input").send_keys(DEMO_PASS)
        driver.find_element(By.ID, "login-btn").click()

        # Filter Samsung devices
        wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Samsung']"))).click()

        # Favorite the Galaxy S20+
        heart = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//p[text()='Galaxy S20+']/ancestor::div[@class='shelf-item']//span[contains(@class, 'bn-heart')]"
        )))
        heart.click()

        # Go to Favorites page
        wait.until(EC.element_to_be_clickable((By.ID, "favorites"))).click()

        # Verify Galaxy S20+ is present in favorites
        wait.until(EC.presence_of_element_located((By.XPATH, "//p[text()='Galaxy S20+']")))

    finally:
        driver.quit()
