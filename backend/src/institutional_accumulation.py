from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import InvalidSessionIdException
import threading
from typing import Dict
from utils.logging import *
from utils.outfiles import *
from utils.scraping import *
from utils.concurrency import *

# constants
threads = 5  # number of concurrent Selenium browser instances to fetch data
timeout = 60
inflows_xpath = "/html/body/div[2]/main/div[2]/article/form/div[4]/div[2]/div[2]/div[1]/div[2]/div/div/div[2]/div/svg/g[3]/g[4]/text[1]/tspan[2]"
outflows_xpath = "/html/body/div[2]/main/div[2]/article/form/div[4]/div[2]/div[2]/div[1]/div[2]/div/div/div[2]/div/svg/g[3]/g[4]/text[3]/tspan[2]"

# print header message to terminal
process_name = "Institutional Accumulation"
process_stage = 5
print_status(process_name, process_stage, True)

# logging data (printed to console after screen finishes)
logs = []

# retreive JSON data from previous screen iteration
df = open_outfile("revenue_growth")

# populate these lists while iterating through symbols
successful_symbols = []
failed_symbols = []
drivers = []

# store local thread data
thread_local = threading.local()


def fetch_institutional_holdings(symbol: str) -> Dict[str, float]:
    "Fetch institutional holdings data for a stock symbol from nasdaq.com."
    # perform get request and stop loading page when data is detected in DOM
    url = f"https://www.marketbeat.com/stocks/NASDAQ/{symbol}/institutional-ownership/"

    driver = get_driver(thread_local, drivers)
    driver.get(url)

    wait_methods = [
        element_is_float(inflows_xpath),
        element_is_float(outflows_xpath),
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
        increased_holders = extract_float(
            driver.find_element(By.XPATH, increased_holders_xpath)
        )
        increased_shares = extract_float(
            driver.find_element(By.XPATH, increased_shares_xpath)
        )
        decreased_holders = extract_float(
            driver.find_element(By.XPATH, decreased_holders_xpath)
        )
        decreased_shares = extract_float(
            driver.find_element(By.XPATH, decreased_shares_xpath)
        )
    except Exception as e:
        logs.append(skip_message(symbol, e))
        return None

    # check for null values in fetched holdings data
    data = [
        increased_holders,
        increased_shares,
        decreased_holders,
        decreased_shares,
    ]

    for datum in data:
        if datum is None:
            logs.append(skip_message(symbol, "insufficient data"))
            return None

    return {
        "Increased": {"Holders": increased_holders, "Shares": increased_shares},
        "Decreased": {"Holders": decreased_holders, "Shares": decreased_shares},
    }


def screen_institutional_accumulation(df_index: int) -> None:
    """Populate stock data lists based on whether the given dataframe row is experiencing institutional demand."""
    # extract stock information from dataframe and fetch institutional holdings info
    row = df.iloc[df_index]

    symbol = row["Symbol"]
    holdings_data = fetch_institutional_holdings(symbol)

    # check for failed GET requests
    if holdings_data is None:
        failed_symbols.append(symbol)
        return

    net_holders = (
        holdings_data["Increased"]["Holders"] - holdings_data["Decreased"]["Holders"]
    )
    net_shares = (
        holdings_data["Increased"]["Shares"] - holdings_data["Decreased"]["Shares"]
    )

    # add institutional holdings info to logs
    logs.append(
        f"""\n{symbol} | Net Institutional Holders: {net_holders:.0f}, Net Institutional Shares: {net_shares:.0f} 
        Increased : holders: {holdings_data["Increased"]["Holders"]:.0f}, shares: {holdings_data["Increased"]["Shares"]:.0f}
        Decreased : holders: {holdings_data["Decreased"]["Holders"]:.0f}, shares: {holdings_data["Decreased"]["Shares"]:.0f}\n"""
    )

    # filter out stocks which are not under institutional accumulation
    if (net_holders < 0) or (net_shares < 0):
        logs.append(filter_message(symbol))
        return

    successful_symbols.append(
        {
            "Symbol": symbol,
            "Company Name": row["Company Name"],
            "Industry": row["Industry"],
            "RS": row["RS"],
            "Price": row["Price"],
            "Market Cap": row["Market Cap"],
            "50-day Average Volume": row["50-day Average Volume"],
            "% Below 52-week High": row["% Below 52-week High"],
            "Net Institutional Holders": int(net_holders),
            "Net Institutional Shares": int(net_shares),
        }
    )


# launch concurrent worker threads to execute the screen
print("\nFetching institutional holdings data . . .\n")
tqdm_thread_pool_map(threads, screen_institutional_accumulation, range(0, len(df)))

# close Selenium web driver sessions
print("\nClosing browser instances . . .\n")
for driver in tqdm(drivers):
    driver.quit()

# create a new dataframe with symbols which satisfied trend criteria
screened_df = pd.DataFrame(successful_symbols)

# serialize data in JSON format and save on machine
create_outfile(screened_df, "institutional_accumulation")

# print log
print("".join(logs))

# print footer message to terminal
print(f"{len(failed_symbols)} symbols failed (insufficient data).")
print(
    f"{len(df) - len(screened_df) - len(failed_symbols)} symbols filtered (not under institutional accumulation)."
)
print(f"{len(screened_df)} symbols passed.")
print_status(process_name, process_stage, False)
