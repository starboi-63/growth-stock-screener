from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from typing import Callable, List
import threading
from threading import local


def get_driver(thread_local: local, drivers: List[WebDriver]) -> WebDriver:
    """Return the web driver attributed to a thread. Create a new web driver if no driver is found."""
    # check the driver associated with the thread
    driver = getattr(thread_local, "driver", None)

    if driver is None:
        # construct new web broswer driver
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.page_load_strategy = "eager"
        driver = webdriver.Firefox(options=options)
        setattr(thread_local, "driver", driver)
        drivers.append(driver)

    return driver


def extract_value(element: WebElement) -> float:
    """Consume a WebElement and return its value as a float."""
    try:
        return float(element.text.replace(",", "").replace(" ", ""))
    except:
        return None


def element_is_float(xpath: str) -> Callable[[WebDriver], bool]:
    """Consumes an xpath and returns a function which consumes a WebDriver and returns true if the DOM element
    at the specified xpath is a float type."""

    def inner(driver: WebDriver) -> bool:
        return type(extract_value(driver.find_element(By.XPATH, xpath))) == float

    return inner


class WaitForAll:
    """Represents an expected condition which is the logical "and" of multiple expected conditions."""

    def __init__(self, methods: List[Callable[[WebDriver], bool]]):
        self.methods = methods

    def __call__(self, driver: WebDriver) -> bool:
        try:
            for method in self.methods:
                if not method(driver):
                    return False
            return True
        except StaleElementReferenceException:
            return False
