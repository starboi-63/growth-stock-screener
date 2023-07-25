import pandas as pd
import os
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from tqdm.asyncio import tqdm_asyncio
from helper_functions import *

# constants
min_market_cap = 1000000000
min_price = 10
min_volume = 100000

# print header message to terminal
process_name = "Liquidity"
process_stage = 2
print_status(process_name, process_stage, True)
print(
    f"""
Minimum market cap to pass: ${min_market_cap / 1000000000:.0f}B
Minimum price to pass: ${min_price:.2f}
Minimum average volume to pass: {min_volume} shares\n
"""
)

# logging data (printed to console after screen finishes)
logs = []

# retreive JSON data from previous screen iteration
df = open_outfile("relative_strengths")

# populate these lists while iterating through symbols
successful_symbols = []
failed_symbols = []


async def fetch(symbol: str, session):
    """coroutine for get request to barchart.com using a stock symbol"""
    url = f"https://www.barchart.com/stocks/quotes/{symbol}/technical-analysis"

    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        logs.append(skip_message(symbol, e))
        failed_symbols.append(symbol)
        return None


def extract_avg_volume(response):
    """extract 50-day average volume from request response"""
    # handle null responses
    if response is None:
        return None

    soup = BeautifulSoup(response, "html.parser")

    # extract 50-day average volume data from html
    tables = soup.find_all("tbody")
    rows = tables[0].find_all("tr")
    row_data = rows[2].find_all("td")
    volume_string = str(row_data[4].contents[0])
    volume_string_cleaned = volume_string.replace(",", "").replace(" ", "")
    volume = int(volume_string_cleaned)
    return volume


async def screen_liquidity(df_index, session):
    """Consumes a row index of the stock dataframe and populates data
    list if the row satisfies liquidity criteria"""
    row = df.iloc[df_index]

    # extract information from dataframe row
    symbol = row["Symbol"]
    name = row["Company Name"]
    price = row["Price"]
    market_cap = row["Market Cap"]
    volume = extract_avg_volume(await fetch(symbol, session))
    industry = row["Industry"]
    rs = row["RS"]

    # check if null values are present in screen criteria
    if volume is None:
        return

    if pd.isna(market_cap):
        logs.append(skip_message(symbol, "couldn't fetch market cap"))
        failed_symbols.append(symbol)
        return

    # print volume info to console
    logs.append(
        f"\n{symbol} | Market Cap: ${market_cap / 1000000000:.1f}B | Price: ${price:.2f} | 50-day Avg. Volume: {volume} shares\n"
    )

    # filter out illiquid stocks
    if (market_cap < min_market_cap) or (price < min_price) or (volume < min_volume):
        return

    successful_symbols.append(
        {
            "Symbol": symbol,
            "Company Name": name,
            "Price": price,
            "Market Cap": market_cap,
            "50-day Average Volume": volume,
            "Industry": industry,
            "RS": rs,
        }
    )


async def main():
    """Screen each stock present in the dataframe based on liquidity criteria"""
    async with aiohttp.ClientSession() as session:
        await tqdm_asyncio.gather(
            *[screen_liquidity(df_index, session) for df_index in range(0, len(df))]
        )


asyncio.run(main())

# create a new dataframe with symbols which satisfied liquidity criteria
screened_df = pd.DataFrame(successful_symbols)

# serialize data in JSON format and save on machine
create_outfile(screened_df, "liquidity")

# print log
print("".join(logs))

# print footer message to terminal
print(f"{len(failed_symbols)} symbols failed (insufficient data).")
print(
    f"{len(df) - len(screened_df) - len(failed_symbols)} symbols filtered (thinly traded or penny stock)."
)
print(f"{len(screened_df)} symbols passed.")
print_status(process_name, process_stage, False)
