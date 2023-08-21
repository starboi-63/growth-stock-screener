from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import threading
import requests
from lxml import html
from typing import Dict
from tqdm import tqdm
from termcolor import cprint, colored
import time
from .utils import *
from ..settings import trend_settings, threads

# constants
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

# print trend iteration settings to terminal
setting_name_color = "dark_grey"
setting_value_color = "light_grey"

trend_1 = " ".join(
    [
        colored("Price >= 50-day SMA:", setting_name_color),
        status(trend_settings["Price >= 50-day SMA"]),
        "|",
        colored("Price >= 200-day SMA:", setting_name_color),
        status(trend_settings["Price >= 200-day SMA"]),
    ]
)

trend_2 = " ".join(
    [
        colored("10-day SMA >= 20-day SMA:", setting_name_color),
        status(trend_settings["10-day SMA >= 20-day SMA"]),
        "|",
        colored("20-day SMA >= 50-day SMA:", setting_name_color),
        status(trend_settings["20-day SMA >= 50-day SMA"]),
    ]
)

trend_3 = " ".join(
    [
        colored("Price Within 50% of 52-week High:", setting_name_color),
        status(trend_settings["Price within 50% of 52-week High"]),
    ]
)

print("\n".join([trend_1, trend_2, trend_3]))

# record start time
start = time.perf_counter()

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


def fetch_moving_averages(symbol: str) -> Dict[str, float]:
    """Fetch moving average data for the given stock symbol from tradingview.com"""
    # configure request url and dynamic wait methods
    url = f"https://www.tradingview.com/symbols/{symbol}/technicals/"

    wait_methods = [
        element_is_float_xpath(sma_10_xpath),
        element_is_float_xpath(sma_20_xpath),
        element_is_float_xpath(sma_50_xpath),
        element_is_float_xpath(sma_200_xpath),
    ]

    combined_wait_method = WaitForAll(wait_methods)

    try:
        # perform get request and stop loading page when data is detected in DOM
        driver = get_driver(thread_local, drivers)
        driver.get(url)
        WebDriverWait(driver, timeout).until(combined_wait_method)
        driver.execute_script("window.stop();")
    except Exception as e:
        logs.append(skip_message(symbol, e))
        return None

    # extract moving averages from DOM
    try:
        sma_10 = extract_float(driver.find_element(By.XPATH, sma_10_xpath))
        sma_20 = extract_float(driver.find_element(By.XPATH, sma_20_xpath))
        sma_50 = extract_float(driver.find_element(By.XPATH, sma_50_xpath))
        sma_200 = extract_float(driver.find_element(By.XPATH, sma_200_xpath))
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
    """Fetch the 52-week high of the given stock symbol from cnbc.com."""
    url = f"https://www.cnbc.com/quotes/{symbol}"

    try:
        response = requests.get(url)
        high_52_week = extract_float(
            extract_element(high_52_week_xpath, response.content)
        )
    except Exception as e:
        logs.append(skip_message(symbol, e))
        return None

    return high_52_week


def screen_trend(df_index: int) -> None:
    """Populate stock data lists based on whether the given dataframe row is in a stage-2 uptrend."""
    # extract stock information from dataframe and fetch trend info
    row = df.iloc[df_index]

    symbol = row["Symbol"]
    trend_data = fetch_moving_averages(symbol)
    high_52_week = fetch_52_week_high(symbol)

    # check for failed GET requests
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

    # set up screen criteria based on global settings
    fails = False
    if trend_settings["Price >= 50-day SMA"]:
        fails = fails or (price < sma_50)
    if trend_settings["Price >= 200-day SMA"]:
        fails = fails or (price < sma_200)
    if trend_settings["10-day SMA >= 20-day SMA"]:
        fails = fails or (sma_10 < sma_20)
    if trend_settings["20-day SMA >= 50-day SMA"]:
        fails = fails or (sma_20 < sma_50)
    if trend_settings["Price within 50% of 52-week High"]:
        fails = fails or (percent_below_high > 50)

    # filter out stocks which are not in a stage-2 uptrend
    if fails:
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
        }
    )


# launch concurrent worker threads to execute the screen
print("\nFetching trend data . . .\n")
tqdm_thread_pool_map(threads, screen_trend, range(0, len(df)))

# close Selenium web driver sessions
print("\nClosing browser instances . . .\n")
for driver in tqdm(drivers):
    driver.quit()

# create a new dataframe with symbols which satisfied trend criteria
screened_df = pd.DataFrame(successful_symbols)

# serialize data in JSON format and save on machine
create_outfile(screened_df, "trend")

# print log
print("".join(logs))

# record end time
end = time.perf_counter()

# print footer message to terminal
cprint(f"{len(failed_symbols)} symbols failed (insufficient data).", "dark_grey")
cprint(
    f"{len(df) - len(screened_df) - len(failed_symbols)} symbols filtered (not in stage-2 uptrend).",
    "dark_grey",
)
cprint(f"{len(screened_df)} symbols passed.", "green")
print_status(process_name, process_stage, False, end - start)
print_divider()
