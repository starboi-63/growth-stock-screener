from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from typing import Callable, List


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
