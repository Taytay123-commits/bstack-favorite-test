import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
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
        desired_capabilities=caps
    )

    try:
        driver.get("https://www.bstackdemo.com")

        # Login
        driver.find_element(By.ID, "signin").click()
        time.sleep(1)
        driver.find_element(By.NAME, "username").send_keys("demouser")
        driver.find_element(By.NAME, "password").send_keys("testingisfun99")
        driver.find_element(By.ID, "login-btn").click()
        time.sleep(2)

        # Filter Samsung
        driver.find_element(By.XPATH, "//p[text()='Samsung']").click()
        time.sleep(2)

        # Favorite Galaxy S20+
        heart = driver.find_element(By.XPATH, "//div[text()='Galaxy S20+']/ancestor::div[@class='shelf-item__details']/following-sibling::div//span")
        heart.click()
        time.sleep(1)

        # Go to Favorites
        driver.find_element(By.ID, "favorites").click()
        time.sleep(2)

        # Verify it's listed
        assert "Galaxy S20+" in driver.page_source

        # Mark test as passed on BrowserStack
        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed","reason": "Galaxy S20+ favorited successfully"}}')

    except Exception as e:
        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed","reason": "%s"}}' % str(e))
        raise
    finally:
        driver.quit()
