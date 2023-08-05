from multiprocessing.pool import ThreadPool
from tqdm import tqdm
from typing import List, Callable
from threading import local
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver


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


def tqdm_thread_pool_map(threads: int, func: Callable, items: List) -> List:
    """Concurrently pass each inputted item into the given function using a thread pool.
    Display a progress bar and return a list of results."""
    with ThreadPool(threads) as pool:
        results = []
        for result in tqdm(pool.imap(func, items), total=len(items)):
            results.append(result)

        return results
