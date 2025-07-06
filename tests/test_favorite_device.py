import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from browserstack_config import USERNAME, ACCESS_KEY, capabilities

@pytest.mark.parametrize("caps", capabilities)
def test_favorite_galaxy_s20(caps):
    browser_name = caps.get("browserName")

    # Define bstack:options (W3C format)
    bstack_options = {
        "userName": USERNAME,
        "accessKey": ACCESS_KEY,
        "buildName": "Galaxy Fav Build",
        "projectName": "Favorites Testing",
        "debug": "true"
    }

    caps["bstack:options"] = bstack_options

    driver = None

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
            # Mobile (no browserName, pass caps directly)
            driver = webdriver.Remote(
                command_executor="https://hub.browserstack.com/wd/hub",
                options=webdriver.ChromeOptions().set_capability("bstack:options", bstack_options)
            )
            for key, value in caps.items():
                driver.capabilities[key] = value

        driver.maximize_window()
        driver.get("https://bstackdemo.com")

        wait = WebDriverWait(driver, 20)

        # Step 1: Click the "Sign In" button to go to the login page
        sign_in_btn = wait.until(EC.element_to_be_clickable((By.ID, "signin")))
        sign_in_btn.click()

        # Step 2: Find the "Username" container and input value
        username_container = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_input = username_container.find_element(By.TAG_NAME, "input")
        username_input.send_keys("bstack-demo-username")
        username_input.send_keys(Keys.RETURN)

        # Step 3: Find the "Password" container and input value
        password_container = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_input = password_container.find_element(By.TAG_NAME, "input")
        password_input.send_keys("bstack-demo-password")
        password_input.send_keys(Keys.RETURN)

        # Step 4: Wait until login is processed
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "username")))

        # Step 5: Filter for Samsung devices
        samsung_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Samsung']/preceding-sibling::input")))
        samsung_checkbox.click()

        # Step 6: Wait for Galaxy S20+ to appear and favorite it
        s20_card = wait.until(EC.presence_of_element_located((By.XPATH, "//p[text()='Galaxy S20+']/ancestor::div[contains(@class, 'shelf-item')]")))
        favorite_icon = s20_card.find_element(By.CSS_SELECTOR, "svg[data-testid='favorite']")
        favorite_icon.click()

        # Step 7: Go to Favorites page
        favorites_link = wait.until(EC.element_to_be_clickable((By.ID, "favorites")))
        favorites_link.click()

        # Step 8: Verify Galaxy S20+ is present in favorites
        wait.until(EC.presence_of_element_located((By.XPATH, "//p[text()='Galaxy S20+']")))

    finally:
        if driver:
            driver.quit()
