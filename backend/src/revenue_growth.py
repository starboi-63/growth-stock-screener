import asyncio
import aiohttp
from aiohttp.client import ClientSession
from tqdm.asyncio import tqdm_asyncio
import pandas as pd
from typing import Dict
from utils.logging import *
from utils.outfiles import *
from utils.calculations import *
from utils.scraping import *

# constants
min_growth_percent = 25
q1_revenue_xpath = (
    "/html/body/div[2]/div[3]/div[1]/div[8]/div[2]/table/tbody/tr[1]/td[2]"
)
q1_prev_revenue_xpath = (
    "/html/body/div[2]/div[3]/div[1]/div[8]/div[2]/table/tbody/tr[5]/td[2]"
)
q2_revenue_xpath = (
    "/html/body/div[2]/div[3]/div[1]/div[8]/div[2]/table/tbody/tr[2]/td[2]"
)
q2_prev_revenue_xpath = (
    "/html/body/div[2]/div[3]/div[1]/div[8]/div[2]/table/tbody/tr[6]/td[2]"
)

# print header message to terminal
process_name = "Revenue Growth"
process_stage = 4
print_status(process_name, process_stage, True)
print(f"Minimum quarterly revenue growth to pass: {min_growth_percent}%")

# logging data (printed to console after screen finishes)
logs = []

# retreive JSON data from previous screen iteration
df = open_outfile("trend")

# populate these lists while iterating through symbols
successful_symbols = []
failed_symbols = []


async def fetch_revenue(
    symbol: str, session: ClientSession
) -> Dict[str, Dict[str, float]]:
    """Fetch quarterly revenue data for the given stock symbol from macrotrends.com."""
    url = f"https://www.macrotrends.net/stocks/charts/{symbol}/upstart-holdings/revenue"
    response = await get(url, session)

    q1_revenue = extract_float(extract_element(q1_revenue_xpath, response))
    q1_prev_revenue = extract_float(extract_element(q1_prev_revenue_xpath, response))
    q2_revenue = extract_float(extract_element(q2_revenue_xpath, response))
    q2_prev_revenue = extract_float(extract_element(q2_prev_revenue_xpath, response))

    # check for null values in fetched revenue data
    if (q1_revenue is None) or (q1_prev_revenue is None) or (q1_prev_revenue is 0):
        return None

    if (q2_revenue is None) or (q2_prev_revenue is None) or (q2_prev_revenue is 0):
        return {"Q1": {"Current": q1_revenue, "Previous": q1_prev_revenue}}

    return {
        "Q1": {"Current": q1_revenue, "Previous": q1_prev_revenue},
        "Q2": {"Current": q2_revenue, "Previous": q2_prev_revenue},
    }


async def screen_revenue_growth(df_index: int, session: ClientSession) -> None:
    """Populate stock data lists based on whether the given dataframe row has strong revenue growth"""
    row = df.iloc[df_index]

    symbol = row["Symbol"]
    revenue_data = await fetch_revenue(symbol, session)

    # handle null values from unsuccessful fetching
    if revenue_data is None:
        failed_symbols.append(symbol)
        return

    q1_revenue_growth = percent_change(
        revenue_data["Q1"]["Previous"], revenue_data["Q1"]["Current"]
    )
    q2_revenue_growth = (
        percent_change(revenue_data["Q2"]["Previous"], revenue_data["Q2"]["Current"])
        if "Q2" in revenue_data
        else None
    )

    # print revenue growth data to console
    logs.append(
        f"""\n{symbol} | Q1 revenue growth: {q1_revenue_growth}%, Q2 revenue growth: {q2_revenue_growth}%
        Q1 : current revenue: ${revenue_data["Q1"]["Current"]}M, previous revenue: ${revenue_data["Q1"]["Previous"]}M
        Q2 : current revenue: ${revenue_data["Q2"]["Current"]}M, previous revenue: ${revenue_data["Q2"]["Previous"]}M"""
    )

    # filter out stocks with low quarterly revenue growth
    if q1_revenue_growth < min_growth_percent:
        logs.append(filter_message(symbol))
        return

    if (q2_revenue_growth is not None) and (q2_revenue_growth < min_growth_percent):
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
            "Revenue Growth % (most recent Q)": q1_revenue_growth,
            "Revenue Growth % (previous Q)": q2_revenue_growth,
            "50-day Average Volume": row["50-day Average Volume"],
            "% Below 52-week High": row["% Below 52-week High"],
        }
    )


async def main() -> None:
    """Screen each stock present in the dataframe based on revenue growth."""
    async with aiohttp.ClientSession() as session:
        await tqdm_asyncio.gather(
            *[
                screen_revenue_growth(df_index, session)
                for df_index in range(0, len(df))
            ]
        )


asyncio.run(main())

# create a new dataframe with symbols which satisfied revenue_growth criteria
screened_df = pd.DataFrame(successful_symbols)

# serialize data in JSON format and save on machine
create_outfile(screened_df, "revenue_growth")

# print log
print("".join(logs))

# print footer message to terminal
print(f"{len(failed_symbols)} symbols failed (insufficient data).")
print(
    f"{len(df) - len(screened_df) - len(failed_symbols)} symbols filtered (revenue growth too low)."
)
print(f"{len(screened_df)} symbols passed.")
print_status(process_name, process_stage, False)
