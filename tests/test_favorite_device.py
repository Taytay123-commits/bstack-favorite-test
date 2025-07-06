import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.browserstack_config import USERNAME, ACCESS_KEY, capabilities


@pytest.mark.parametrize("caps", capabilities)
def test_favorite_galaxy_s20(caps):
    caps["browserstack.user"] = USERNAME
    caps["browserstack.key"] = ACCESS_KEY
    caps["build"] = "Galaxy Fav Build"
    caps["project"] = "Favorites Testing"
    caps["browserstack.debug"] = "true"

    driver = webdriver.Remote(
        command_executor="http://hub.browserstack.com/wd/hub",
        options=webdriver.ChromeOptions() if caps.get("browserName") == "Chrome" else None,
        desired_capabilities=caps
    )

    try:
        wait = WebDriverWait(driver, 15)
        driver.get("https://www.bstackdemo.com")

        # Login
        wait.until(EC.element_to_be_clickable((By.ID, "signin"))).click()
        wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys("demouser")
        driver.find_element(By.ID, "password").send_keys("testingisfun99")
        driver.find_element(By.ID, "login-btn").click()

        # Filter by Samsung
        samsung_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Samsung']")))
        samsung_checkbox.click()
        time.sleep(2)  # Allow product grid to update

        # Favorite Galaxy S20+
        heart_xpath = "//p[text()='Galaxy S20+']/ancestor::div[contains(@class, 'shelf-item')]//span[contains(@class, 'favorite')]"
        heart = wait.until(EC.element_to_be_clickable((By.XPATH, heart_xpath)))
        heart.click()

        # Go to Favorites
        fav_link = wait.until(EC.element_to_be_clickable((By.ID, "favorites"))).click()

        # Verify Galaxy S20+ is in Favorites
        fav_product = wait.until(EC.presence_of_element_located((By.XPATH, "//p[text()='Galaxy S20+']")))
        assert fav_product.is_displayed(), "Galaxy S20+ not found in favorites!"

    finally:
        driver.quit()
