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
    if (q1_revenue is None) or (q1_prev_revenue is None):
        return None

    if (q2_revenue is None) or (q2_prev_revenue is None):
        return {"Q1": {"Current": q1_revenue, "Previous": q1_prev_revenue}}

    return {
        "Q1": {"Current": q1_revenue, "Previous": q1_prev_revenue},
        "Q2": {"Current": q2_revenue, "Previous": q2_prev_revenue},
    }


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        print(await get("NVDA", session))


asyncio.run(main())
