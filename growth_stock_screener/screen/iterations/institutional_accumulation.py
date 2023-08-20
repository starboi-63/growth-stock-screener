from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import threading
import requests
from tqdm import tqdm
from typing import Dict
import time
from termcolor import colored, cprint
from .utils import *

# constants
threads = 5  # number of concurrent Selenium browser instances to fetch data
timeout = 60
exchange_xpath = "/html/body/div[3]/div[2]/div[2]/div/div[1]/div[2]/span[2]"
inflows_css = ".info-slider-bought-text > tspan:nth-child(2)"
outflows_css = ".info-slider-sold-text > tspan:nth-child(2)"

# print header message to terminal
process_name = "Institutional Accumulation"
process_stage = 5
print_status(process_name, process_stage, True)

# record start time
start = time.perf_counter()

# logging data (printed to console after screen finishes)
logs = []

# retreive JSON data from previous screen iteration
df = open_outfile("revenue_growth")

# populate these lists while iterating through symbols
successful_symbols = []
failed_symbols = []
symbols_under_accumulation = []
drivers = []

# store local thread data
thread_local = threading.local()


def fetch_exchange(symbol: str) -> str:
    "Fetch the exchange that a stock symbol is listed on (either NASDAQ or NYSE)."
    exchanges = ["NASDAQ", "NYSE"]

    for exchange in exchanges:
        url = f"https://www.marketbeat.com/stocks/{exchange}/{symbol}/"
        try:
            response = requests.get(url, allow_redirects=False, timeout=timeout)
        except Exception:
            continue

        if response.status_code == 200:
            return exchange

    logs.append(skip_message(symbol, "couldn't fetch exchange"))
    return None


def fetch_institutional_holdings(symbol: str) -> Dict[str, float]:
    "Fetch institutional holdings data for a stock symbol from marketbeat.com."
    # perform get request and stop loading page when data is detected in DOM
    exchange = fetch_exchange(symbol)

    if exchange is None:
        return None

    url = f"https://www.marketbeat.com/stocks/{exchange}/{symbol}/institutional-ownership/"

    driver = get_driver(thread_local, drivers)
    driver.get(url)

    wait_methods = [
        element_is_float_css(inflows_css),
        element_is_float_css(outflows_css),
    ]

    combined_wait_method = WaitForAll(wait_methods)

    try:
        WebDriverWait(driver, timeout).until(combined_wait_method)
        driver.execute_script("window.stop();")
    except TimeoutException:
        logs.append(skip_message(symbol, "request timed out"))
        return None

    # extract institutional holdings information from DOM
    try:
        inflows = extract_dollars(driver.find_element(By.CSS_SELECTOR, inflows_css))
        outflows = extract_dollars(driver.find_element(By.CSS_SELECTOR, outflows_css))
    except Exception as e:
        logs.append(skip_message(symbol, e))
        return None

    if (inflows is None) or (outflows is None):
        logs.append(skip_message(symbol, "insufficient data"))
        return None

    return {"Inflows": inflows, "Outflows": outflows}


def screen_institutional_accumulation(df_index: int) -> None:
    """Populate stock data lists based on whether the given dataframe row is experiencing institutional demand."""
    # extract stock information from dataframe and fetch institutional holdings info
    row = df.iloc[df_index]

    symbol = row["Symbol"]
    holdings_data = fetch_institutional_holdings(symbol)

    # check for failed GET requests
    if holdings_data is None:
        failed_symbols.append(symbol)
    else:
        net_inflows = holdings_data["Inflows"] - holdings_data["Outflows"]

        # add institutional holdings info to logs
        logs.append(
            f"""\n{symbol} | Net Institutional Inflows (most recent Q): ${net_inflows:,.0f} 
            Inflows: ${holdings_data["Inflows"]:,.0f}, Outflows: ${holdings_data["Outflows"]:,.0f}\n"""
        )

        # mark stocks which are under institutional accumulation
        if net_inflows >= 0:
            logs.append(
                message(
                    colored(
                        f"{symbol} was under institutional accumulation last quarter.",
                        "dark_grey",
                    )
                )
            )
            symbols_under_accumulation.append(symbol)

    successful_symbols.append(
        {
            "Symbol": symbol,
            "Company Name": row["Company Name"],
            "Industry": row["Industry"],
            "RS": row["RS"],
            "Price": row["Price"],
            "Market Cap": row["Market Cap"],
            "Net Institutional Inflows": None
            if (holdings_data is None)
            else net_inflows,
            "Revenue Growth % (most recent Q)": row["Revenue Growth % (most recent Q)"],
            "Revenue Growth % (previous Q)": row["Revenue Growth % (previous Q)"],
            "50-day Average Volume": row["50-day Average Volume"],
            "% Below 52-week High": row["% Below 52-week High"],
        }
    )


# launch concurrent worker threads to execute the screen
print("Fetching institutional holdings data . . .\n")
tqdm_thread_pool_map(threads, screen_institutional_accumulation, range(0, len(df)))

# close Selenium web driver sessions
print("\nClosing browser instances . . .\n")
for driver in tqdm(drivers):
    driver.quit()

# create a new dataframe with symbols which are under institutional accumulation
screened_df = pd.DataFrame(successful_symbols)

# serialize data in JSON format and save on machine
create_outfile(screened_df, "institutional_accumulation")

# print log
print("".join(logs))

# record end time
end = time.perf_counter()

# print footer message to terminal
cprint(f"{len(failed_symbols)} symbols failed (insufficient data).", "dark_grey")
cprint(
    f"{len(df) - len(failed_symbols) - len(symbols_under_accumulation)} symbols were not under institutional accumulation last quarter.",
    "dark_grey",
)
cprint(
    f"{len(symbols_under_accumulation)} symbols were under institutional accumulation last quarter.",
    "green",
)
cprint(f"{len(screened_df)} symbols passed.", "green")
print_status(process_name, process_stage, False, end - start)
print_divider()
