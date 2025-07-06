import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions
from utils.browserstack_config import USERNAME, ACCESS_KEY, capabilities


@pytest.mark.parametrize("caps", capabilities)
def test_favorite_galaxy_s20(caps):
    # Set authentication & build info
    caps["browserstack.user"] = USERNAME
    caps["browserstack.key"] = ACCESS_KEY
    caps["build"] = "Galaxy Fav Build"
    caps["project"] = "Favorites Testing"
    caps["browserstack.debug"] = "true"

    # Choose the right browser options
    browser = caps.get("browser", "Chrome").lower()
    if browser == "firefox":
        options = FirefoxOptions()
    else:
        options = ChromeOptions()

    # Add all capabilities
    for key, value in caps.items():
        options.set_capability(key, value)

    # Connect to BrowserStack
    driver = webdriver.Remote(
        command_executor="http://hub.browserstack.com/wd/hub",
        options=options
    )

    # Simple test logic
    driver.get("https://www.google.com")
    assert "Google" in driver.title

    driver.quit()

