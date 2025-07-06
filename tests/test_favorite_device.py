import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from browserstack_config import USERNAME, ACCESS_KEY, DEMO_PASS, capabilities


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

    caps["bstack:options"] = bstack_options

    try:
        # Desktop browsers
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
            # Mobile devices
            options = webdriver.ChromeOptions()
            for key, value in caps.items():
                options.set_capability(key, value)

            driver = webdriver.Remote(
                command_executor="https://hub.browserstack.com/wd/hub",
                options=options
            )

        driver.maximize_window()
        wait = WebDriverWait(driver, 20)

        # Step 1: Go to the homepage
        driver.get("https://bstackdemo.com")

        # Step 2: Click "Sign In" button
        sign_in_button = wait.until(EC.element_to_be_clickable((By.ID, "signin")))
        sign_in_button.click()

        # Step 3: Find the "username" container and send credentials
        username_container = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_input = username_container.find_element(By.TAG_NAME, "input")
        username_input.send_keys(USERNAME)
        username_input.send_keys(Keys.ENTER)

        # Step 4: Find the "password" container and send credentials
        password_container = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_input = password_container.find_element(By.TAG_NAME, "input")
        password_input.send_keys(DEMO_PASS)
        password_input.send_keys(Keys.ENTER)

        # Step 5: Filter for "Samsung"
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Samsung']"))).click()

        # Step 6: Favorite "Galaxy S20+"
        heart = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//p[text()='Galaxy S20+']/../../..//span[contains(@class,'favorite')]")
        ))
        heart.click()

        # Step 7: Go to Favorites
        favorites_link = wait.until(EC.element_to_be_clickable((By.ID, "favorites")))
        favorites_link.click()

        # Step 8: Verify "Galaxy S20+" is listed
        wait.until(EC.visibility_of_element_located((By.XPATH, "//p[text()='Galaxy S20+']")))

    finally:
        driver.quit()

