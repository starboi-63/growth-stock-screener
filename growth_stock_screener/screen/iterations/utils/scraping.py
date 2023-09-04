from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from typing import Callable, List
from aiohttp.client import ClientSession
from lxml import html
import re
import yfinance as yf
import pandas as pd


async def get(url: str, session: ClientSession, headers=None, json=False) -> str:
    """Send a GET request for the given url and return the response as a string. Setting 'json' to 'True' will return a json object."""
    try:
        async with session.get(url, headers=headers) as response:
            if json:
                return await response.json()
            else:
                return await response.text()
    except Exception:
        return None


def extract_element(xpath: str, response: str) -> WebElement:
    """Return the WebElement at a given xpath from a GET request response."""
    if response is None:
        return None

    dom = html.fromstring(response)

    try:
        element = dom.xpath(xpath)[0]
        return element
    except Exception:
        return None


def extract_float(element: WebElement) -> float:
    """Return the content stored in a WebElement as a float."""
    try:
        cleaned_content = re.sub(r"[^0-9.]", "", element.text)
        return float(cleaned_content)
    except Exception:
        return None


def extract_dollars(element: WebElement) -> float:
    """Return the financial content stored in a WebElement of the form "...B", "...M", "...k", or "..." as a float representing dollars."""
    try:
        cleaned_content = re.sub(r"[^0-9.BMk]", "", element.text)
        nums_only = re.sub(r"[^0-9.]", "", element.text)
        last_char = cleaned_content[-1]

        if last_char == "B":
            return float(nums_only) * 1000000000
        elif last_char == "M":
            return float(nums_only) * 1000000
        elif last_char == "k":
            return float(nums_only) * 1000
        elif last_char.isdigit():
            return float(nums_only)
        else:
            return None
    except Exception:
        return None


def element_is_float_xpath(xpath: str) -> Callable[[WebDriver], bool]:
    """Return a function which consumes a WebDriver and returns true if the DOM element
    at the specified xpath is a float type."""

    def inner(driver: WebDriver) -> bool:
        element = driver.find_element(By.XPATH, xpath)
        return type(extract_float(element)) == float

    return inner


def element_is_float_css(css_selector: str) -> Callable[[WebDriver], bool]:
    """Return a function which consumes a WebDriver and returns true if the DOM element
    at the specified css-selector is a float type."""

    def inner(driver: WebDriver) -> bool:
        element = driver.find_element(By.CSS_SELECTOR, css_selector)
        return type(extract_float(element)) == float

    return inner


class WaitForAll:
    """Expected condition which is the logical "and" of multiple expected conditions."""

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


def yf_download_batches(
    batch_size: int, symbol_list: List[str], timeout: int
) -> pd.DataFrame:
    """Download historical stock price data in batches using yfinance."""

    def download_batch(start: int, end: int) -> pd.DataFrame:
        """Download a batch of historical stock price data from start to end - 1."""
        print(
            f"Batch {batch_number}: Symbols {start + 1} to {end} ({symbol_list[start]} — {symbol_list[end - 1]})"
        )
        batch = yf.download(
            [symbol_list[i] for i in range(start, end)], period="2y", timeout=timeout
        )
        print()
        return batch

    dfs = []
    start = 0
    end = min(batch_size, len(symbol_list))
    batch_number = 1

    # loop-and-a-half
    while end < len(symbol_list):
        dfs.append(download_batch(start, end))

        # increment counters
        start += batch_size
        end = min(end + batch_size, len(symbol_list))
        batch_number += 1

    dfs.append(download_batch(start, end))

    # concatenate the 'Close' columns in each DataFrame
    price_dfs = map(lambda df: df["Close"], dfs)
    return pd.concat(price_dfs, axis=1)
