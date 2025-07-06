import os

USERNAME = os.environ.get("BROWSERSTACK_USERNAME")  # For BrowserStack API
ACCESS_KEY = os.environ.get("BROWSERSTACK_ACCESS_KEY")
DEMO_USER = os.environ.get("bstack-demo-username")  # For UI login
DEMO_PASS = os.environ.get("bstack-demo-password")  # For UI login

capabilities = [
    {
        "browserName": "Chrome",
        "browserVersion": "latest",
        "os": "Windows",
        "osVersion": "10"
    },
    {
        "browserName": "Firefox",
        "browserVersion": "latest",
        "os": "OS X",
        "osVersion": "Ventura"
    },
    {
        "deviceName": "Samsung Galaxy S22",
        "realMobile": "true",
        "osVersion": "12.0"
    }
]
