import pandas as pd
import asyncio
import aiohttp
from aiohttp.client import ClientSession
from tqdm.asyncio import tqdm_asyncio
from utils.logging import *
from utils.outfiles import *
from utils.scraping import *

# constants
min_market_cap = 1000000000
min_price = 10
min_volume = 100000
volume_xpath = "/html/body/main/div/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/barchart-table-scroll/table/tbody/tr[3]/td[5]"

# print header message to terminal
process_name = "Liquidity"
process_stage = 2
print_status(process_name, process_stage, True)
print(
    f"""Minimum market cap to pass: ${min_market_cap / 1000000000:.0f}B
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


async def fetch_volume(symbol: str, session: ClientSession) -> int:
    """Consume a stock symbol and aiohttp session and return the 50-day average volume of the given symbol."""
    url = f"https://www.barchart.com/stocks/quotes/{symbol}/technical-analysis"

    try:
        response = await get(url, session)
        volume_element = extract_element(volume_xpath, response)
        volume = int(extract_float(volume_element))
        return volume
    except Exception as e:
        logs.append(skip_message(symbol, e))
        return None


async def screen_liquidity(df_index: int, session: ClientSession) -> None:
    """Consume a row index of the stock dataframe and populate
    data lists if the row satisfies liquidity criteria."""
    row = df.iloc[df_index]

    # extract important information from dataframe row
    symbol = row["Symbol"]
    price = row["Price"]
    market_cap = row["Market Cap"]
    volume = await fetch_volume(symbol, session)

    # check if null values are present in screen criteria
    if volume is None:
        failed_symbols.append(symbol)
        return

    if pd.isna(market_cap) or market_cap == "":
        logs.append(skip_message(symbol, "couldn't fetch market cap"))
        failed_symbols.append(symbol)
        return

    # convert market cap from string literal to float
    market_cap = float(market_cap)

    # print volume info to console
    logs.append(
        f"\n{symbol} | Market Cap: ${market_cap / 1000000000:.1f}B | Price: ${price:.2f} | 50-day Avg. Volume: {volume} shares\n"
    )

    # filter out illiquid stocks
    if (market_cap < min_market_cap) or (price < min_price) or (volume < min_volume):
        logs.append(filter_message(symbol))
        return

    successful_symbols.append(
        {
            "Symbol": symbol,
            "Company Name": row["Company Name"],
            "Price": price,
            "Market Cap": market_cap,
            "50-day Average Volume": volume,
            "Industry": row["Industry"],
            "RS": row["RS"],
        }
    )


async def main() -> None:
    """Screen each stock present in the dataframe based on liquidity criteria."""
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
