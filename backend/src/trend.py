from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
import threading
from multiprocessing.pool import ThreadPool
from tqdm import tqdm
import requests
from lxml import html
from utils.logging import *
from utils.outfiles import *
from utils.calculations import *
from utils.scraping import *

# constants
threads = 10  # number of concurrent Selenium browser instances to fetch data
timeout = 30
sma_10_xpath = "/html/body/div[3]/div[4]/div[2]/div[2]/div/section/div/div[6]/div[2]/div[2]/table/tbody/tr[3]/td[2]"
sma_20_xpath = "/html/body/div[3]/div[4]/div[2]/div[2]/div/section/div/div[6]/div[2]/div[2]/table/tbody/tr[5]/td[2]"
sma_50_xpath = "/html/body/div[3]/div[4]/div[2]/div[2]/div/section/div/div[6]/div[2]/div[2]/table/tbody/tr[9]/td[2]"
sma_200_xpath = "/html/body/div[3]/div[4]/div[2]/div[2]/div/section/div/div[6]/div[2]/div[2]/table/tbody/tr[13]/td[2]"
high_52_week_xpath = "/html/body/div[2]/div/div[1]/div[3]/div/div/div[1]/div[5]/div[2]/section/div[1]/ul/li[5]/span[2]"

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
drivers = []

# store local thread data
thread_local = threading.local()


def fetch_moving_averages(symbol: str) -> dict:
    """Consume a stock symbol and return its moving average data as a dictionary."""
    url = f"https://www.tradingview.com/symbols/{symbol}/technicals/"
    # perform get request and stop loading page when data table is detected in DOM
    driver = get_driver(thread_local, drivers)
    driver.get(url)

    wait_methods = [
        element_is_float(sma_10_xpath),
        element_is_float(sma_20_xpath),
        element_is_float(sma_50_xpath),
        element_is_float(sma_200_xpath),
    ]

    combined_wait_method = WaitForAll(wait_methods)

    try:
        WebDriverWait(driver, timeout).until(combined_wait_method)
        driver.execute_script("window.stop();")
    except TimeoutException:
        logs.append(skip_message(symbol, "request timed out"))
        return None

    try:
        sma_10 = extract_value(driver.find_element(By.XPATH, sma_10_xpath))
        sma_20 = extract_value(driver.find_element(By.XPATH, sma_20_xpath))
        sma_50 = extract_value(driver.find_element(By.XPATH, sma_50_xpath))
        sma_200 = extract_value(driver.find_element(By.XPATH, sma_200_xpath))
    except Exception as e:
        logs.append(skip_message(symbol, e))
        return None

    trend_data = {
        "10-day SMA": sma_10,
        "20-day SMA": sma_20,
        "50-day SMA": sma_50,
        "200-day SMA": sma_200,
    }

    # check for null values in fetched trend data
    for data in trend_data.values():
        if data is None:
            logs.append(skip_message(symbol, "insufficient data"))
            return None

    return trend_data


def fetch_52_week_high(symbol: str) -> float:
    """Consume a stock symbol and return its 52-week high."""
    url = f"https://www.cnbc.com/quotes/{symbol}"
    response = requests.get(url)

    try:
        dom = html.fromstring(response.content)
        high_52_week_elt = dom.xpath(high_52_week_xpath)[0]
        high_52_week = extract_value(high_52_week_elt)
    except Exception as e:
        logs.append(skip_message(symbol, e))
        return None

    return high_52_week


def screen_trend(df_index: int) -> None:
    """Consume a stock symbol and populate data lists based on whether the stock
    is in a stage-2 uptrend."""
    # extract stock information from dataframe and fetch trend info
    row = df.iloc[df_index]

    symbol = row["Symbol"]
    trend_data = fetch_moving_averages(symbol)
    high_52_week = fetch_52_week_high(symbol)

    if (trend_data is None) or (high_52_week is None):
        failed_symbols.append(symbol)
        return

    price = row["Price"]
    sma_10 = trend_data["10-day SMA"]
    sma_20 = trend_data["20-day SMA"]
    sma_50 = trend_data["50-day SMA"]
    sma_200 = trend_data["200-day SMA"]

    percent_below_high = -1 * percent_change(high_52_week, price)

    # print trend info to console
    logs.append(
        f"""\n{symbol} | 10-day SMA: ${sma_10}, 20-day SMA: ${sma_20}, 50-day SMA: ${sma_50}, 200-day SMA: ${sma_200}
        Current Price: ${price:.2f}, 52-week high: ${high_52_week}, Percent Below 52-week High: {percent_below_high:.0f}%\n"""
    )

    # filter out stocks which are not in a stage-2 uptrend
    if (
        (price < sma_50)
        or (price < sma_200)
        or (sma_10 < sma_20)
        or (sma_20 < sma_50)
        or (percent_below_high > 50)
    ):
        logs.append(filter_message(symbol))
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
            "10-day SMA": sma_10,
            "20-day SMA": sma_20,
            "50-day SMA": sma_50,
            "200-day SMA": sma_200,
            "52-week high": high_52_week,
        }
    )


with ThreadPool(threads) as pool:
    # tqdm requires an array to track finished threads in order to create a progress bar
    results_tqdm = []
    for result in tqdm(pool.imap(screen_trend, range(0, len(df))), total=len(df)):
        results_tqdm.append(result)

# create a new dataframe with symbols which satisfied trend criteria
screened_df = pd.DataFrame(successful_symbols)

# serialize data in JSON format and save on machine
create_outfile(screened_df, "trend")

# print log
print("".join(logs))

# print footer message to terminal
print(f"{len(failed_symbols)} symbols failed (insufficient data).")
print(
    f"{len(df) - len(screened_df) - len(failed_symbols)} symbols filtered (not in stage-2 uptrend)."
)
print(f"{len(screened_df)} symbols passed.")
print_status(process_name, process_stage, False)

# close Selenium web driver sessions
for driver in drivers:
    driver.quit()
