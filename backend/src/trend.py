from helper_functions import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import threading
from multiprocessing.pool import ThreadPool
from tqdm import tqdm

# constants
threads = 10  # number of concurrent Selenium browser instances to fetch data
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

# populate these lists while iterating through symbols
successful_symbols = []
failed_symbols = []

# store local thread data
thread_local = threading.local()


def get_driver():
    """returns the web driver attributed to a thread; creates a new
    web driver if no driver is found"""
    # check the driver associated with the thread
    driver = getattr(thread_local, "driver", None)

    if driver is None:
        # construct new web broswer driver
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.page_load_strategy = "none"
        driver = webdriver.Firefox(options=options)
        setattr(thread_local, "driver", driver)

    return driver


def extract_value(td) -> float:
    """consumes a beautiful soup table-data object from movingaverages.com
    and returns the value contained in it"""
    raw_value = list(td.children)[1].contents[0]
    return float(raw_value)


def fetch(symbol: str) -> dict:
    """consumes a stock symbol and returns moving average data and 52-week high as a dictionary"""
    url = f"https://www.movingaverages.com/pivot-points/{symbol}"
    # perform get request and stop loading page when data table is detected in DOM
    driver = get_driver()
    driver.get(url)

    try:
        data_present = EC.presence_of_element_located((By.XPATH, moving_averages_xpath))
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

    trend_data = {
        "10-day EMA": ema_10,
        "21-day EMA": ema_21,
        "50-day SMA": sma_50,
        "200-day SMA": sma_200,
        "52-week high": high_52_week,
    }

    # check for null values in fetched trend data
    for data in trend_data.values():
        if data is None:
            logs.append(skip_message(symbol, "insufficient data"))
            failed_symbols.append(symbol)
            return None

    return trend_data


def screen_trend(df_index: int):
    """consumes a stock symbol and populates data lists based on whether the stock
    is in a stage-2 uptrend"""
    # extract stock information from dataframe and fetch trend info
    row = df.iloc[df_index]

    symbol = row["Symbol"]
    trend_data = fetch(symbol)

    if trend_data is None:
        return

    price = row["Price"]
    ema_10 = trend_data["10-day EMA"]
    ema_21 = trend_data["21-day EMA"]
    sma_50 = trend_data["50-day SMA"]
    sma_200 = trend_data["200-day SMA"]
    high_52_week = trend_data["52-week high"]

    percent_below_high = -1 * percent_change(high_52_week, price)

    # print trend info to console
    logs.append(
        f"""\n{symbol} | 10-day EMA: ${ema_10}, 21-day EMA: ${ema_21}, 50-day SMA: ${sma_50}, 200-day SMA: ${sma_200}
        52-week high: ${high_52_week}, Percent Below 52-week High: {percent_below_high:.0f}%\n"""
    )

    # filter out stocks which are not in a stage-2 uptrend
    if (
        (price < sma_50)
        or (price < sma_200)
        or (ema_10 < ema_21)
        or (ema_21 < sma_50)
        or (percent_below_high > 50)
    ):
        return

    successful_symbols.append(
        {
            "Symbol": symbol,
            "Company Name": row["Company Name"],
            "Industry": row["Industry"],
            "RS": row["RS"],
            "Price": price,
            "Market Cap": row["Market Cap"],
            "50-day Average Volume": row["50-day Average Volume"],
            "% Below 52-week High": percent_below_high,
        }.update(trend_data)
    )


with ThreadPool(threads) as pool:
    # tqdm requires an array to track finished threads in order to create a progress bar
    results_tqdm = []
    for result in tqdm(pool.imap(screen_trend, range(0, 10)), total=10):
        results_tqdm.append(result)

# print log
print("".join(logs))
