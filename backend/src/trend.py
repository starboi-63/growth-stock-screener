from helper_functions import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from threading import Thread

# constants
max_threads = 10  # number of concurrent Selenium browser instances to fetch data
timeout = 30
moving_averages_xpath = "/html/body/main/div/div[2]/div/div[2]/div[4]/div/div[2]/div/div/div/div[4]/div/div[2]/div/div[1]/table/tbody"

# print header message to terminal
process_name = "Trend"
process_stage = 3
print_status(process_name, process_stage, True)

# logging data (printed to console after screen finishes)
logs = []

# retreive JSON data from previous screen iteration
df = open_outfile("liquidity")

# configure selenium to use a headless Firefox browser instance to request data
options = webdriver.FirefoxOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.page_load_strategy = "none"


def extract_value(td) -> float:
    """consumes a beautiful soup table-data object from movingaverages.com
    and returns the value contained in it"""
    raw_value = list(td.children)[1].contents[0]
    return float(raw_value)


def fetch(symbol: str) -> dict:
    """consumes a stock symbol and returns moving average data and 52-week high as a dictionary"""
    url = f"https://www.movingaverages.com/pivot-points/{symbol}"

    with webdriver.Firefox(options=options) as driver:
        # perform get request and stop loading page when data table is detected in DOM
        driver.get(url)

        try:
            data_present = EC.presence_of_element_located(
                (By.XPATH, moving_averages_xpath)
            )
            WebDriverWait(driver, timeout).until(data_present)
            driver.execute_script("window.stop();")
        except TimeoutException:
            logs.append(skip_message(symbol, "request timed out"))
            failed_symbols.append(symbol)
            return None

        # extract moving averages and 52-week high from response
        soup = BeautifulSoup(driver.page_source, "html.parser")

        ema_10 = extract_value(soup.find("td", class_="ma10"))
        ema_21 = extract_value(soup.find("td", class_="ma21"))
        sma_50 = extract_value(soup.find("td", class_="ma50"))
        sma_200 = extract_value(soup.find("td", class_="ma200"))
        high_52_week = float(
            soup.find("tr", attrs={"data-marker": "52wkHigh"})["data-value"]
        )

        return {
            "10-day EMA": ema_10,
            "21-day EMA": ema_21,
            "50-day SMA": sma_50,
            "200-day SMA": sma_200,
            "52-week high": high_52_week,
        }


result = fetch("NVDA")
print(result)
print(type(result))

running_threads = 0

# populate these lists while iterating through symbols
successful_symbols = []
failed_symbols = []
