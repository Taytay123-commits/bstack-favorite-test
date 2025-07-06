import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("BROWSERSTACK_USERNAME")
ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")

capabilities = [
    {
        "browser": "Chrome",
        "browser_version": "latest",
        "os": "Windows",
        "os_version": "10",
        "name": "Windows Chrome Test"
    },
    {
        "browser": "Firefox",
        "browser_version": "latest",
        "os": "OS X",
        "os_version": "Ventura",
        "name": "macOS Firefox Test"
    },
    {
        "device": "Samsung Galaxy S22",
        "real_mobile": "true",
        "os_version": "12.0",
        "name": "Mobile Test"
    }
]
