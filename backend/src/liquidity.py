import requests
from requests.exceptions import Timeout
import pandas as pd
import json
import os
import asyncio
import aiohttp

# request constants
timeout = 30
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
}

# retreive JSON data from previous screen iteration
json_path = os.path.join(os.getcwd(), "backend", "json", "relative_strengths.json")
df = pd.read_json(json_path)

# populate these lists while iterating through symbols
successful_symbols = []
names = []
mkt_caps = []
industries = []
prices = []
avg_volumes = []
rs_list = []
failed_symbols = []


async def get_response(symbol: str, session):
    """coroutine for get request to barchart.com using a stock symbol"""
    url = f"https://www.barchart.com/stocks/quotes/{symbol}/technical-analysis"

    try:
        response = await session.get(url)
        return await response.text()
    except Exception as e:
        failed_symbols.append(symbol)
        return None


def extract_avg_volume(response):
    """extract 50-day volume SMA from request response"""
    print(response)


async def screen_liquidity(df_index, session):
    """Consumes a row index of the stock dataframe and populates data
    lists if the row satisfies liquidity criteria"""
    row = df.iloc[df_index]

    symbol = row["Symbol"]
    name = row["Company Name"]
    mkt_cap = row["Market Cap"]
    industry = row["Industry"]
    price = row["Price"]
    rs = row["RS"]

    if pd.isna(mkt_cap):
        failed_symbols.append(symbol)
        return None

    if mkt_cap < 1000000000 or price < 10:
        return None


async def main():
    async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
        await asyncio.gather(
            *[screen_liquidity(df_index, session) for df_index in range(0, len(df))]
        )
