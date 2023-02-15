import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver

from abstract.selenium_listener import MyListener


def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default='chrome',
                     help="Choose browser: chrome or firefox")


@pytest.fixture
def get_chrome_options():
    options = chrome_options()
    options.add_argument('chrome')  # Use headless if you do not need a browser UI
    options.add_argument('--start-maximized')
    options.add_argument('--window-size=1650,900')
    return options


@pytest.fixture
def get_webdriver(request, get_chrome_options):
    browser_name = request.config.getoption("browser_name")
    driver = None
    if browser_name == "chrome":
        options = get_chrome_options
        driver = webdriver.Chrome(options=options)
    return driver


@pytest.fixture(autouse=True)
def setup(request, get_webdriver):
    driver = get_webdriver
    driver = EventFiringWebDriver(driver, MyListener())
    if request.cls is not None:
        request.cls.driver = driver
    yield driver
    driver.quit()
