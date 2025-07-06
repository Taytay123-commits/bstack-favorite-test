import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

    # Attach bstack:options
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
            # For mobile devices, use options and set all capabilities directly
            mobile_options = webdriver.ChromeOptions()
            for key, value in caps.items():
                mobile_options.set_capability(key, value)

            driver = webdriver.Remote(
                command_executor="https://hub.browserstack.com/wd/hub",
                options=mobile_options
            )

        driver.get("https://bstackdemo.com")
        wait = WebDriverWait(driver, 20)

        # Click "Sign In" in the top right to bring up the login modal
        sign_in = wait.until(EC.element_to_be_clickable((By.ID, "signin")))
        sign_in.click()

        # Fill in credentials and log in
        wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys("demouser")
        driver.find_element(By.ID, "password").send_keys(DEMO_PASS)
        driver.find_element(By.ID, "login-btn").click()

        # Filter Samsung devices
        wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Samsung']"))).click()

        # Favorite the Galaxy S20+
        heart = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Galaxy S20+']/ancestor::div[@class='shelf-item']//span[contains(@class, 'bn-heart')]")))
        heart.click()

        # Navigate to Favorites
        fav_link = wait.until(EC.element_to_be_clickable((By.ID, "favorites")))
        fav_link.click()

        # Verify Galaxy S20+ is present in favorites
        wait.until(EC.presence_of_element_located((By.XPATH, "//p[text()='Galaxy S20+']")))

    finally:
        driver.quit()
