import pandas as pd
import os
import asyncio
import aiohttp
from bs4 import BeautifulSoup


# retreive JSON data from previous screen iteration
json_path = os.path.join(os.getcwd(), "backend", "json", "relative_strengths.json")
df = pd.read_json(json_path)

# populate these lists while iterating through symbols
successful_symbols = []
# names = []
# mkt_caps = []
# industries = []
# prices = []
# avg_volumes = []
# rs_list = []
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
    # handle null responses
    if response is None:
        return None

    soup = BeautifulSoup(response, "html.parser")

    # extract 50-day volume SMA data from html
    tables = soup.find_all("tbody")
    rows = tables[0].find_all("tr")
    row_data = rows[2].find_all("td")
    vol_string = str(row_data[4].contents[0])
    vol_string_cleaned = vol_string.replace(",", "").replace(" ", "")
    volume = int(vol_string_cleaned)
    return volume


async def main():
    async with aiohttp.ClientSession() as session:
        response = await get_response("NVDA", session)
        extract_avg_volume(response)


# async def screen_liquidity(df_index, session):
#     """Consumes a row index of the stock dataframe and populates data
#     lists if the row satisfies liquidity criteria"""
#     row = df.iloc[df_index]

#     symbol = row["Symbol"]
#     name = row["Company Name"]
#     mkt_cap = row["Market Cap"]
#     industry = row["Industry"]
#     price = row["Price"]
#     rs = row["RS"]

#     if pd.isna(mkt_cap):
#         failed_symbols.append(symbol)
#         return None

#     if mkt_cap < 1000000000 or price < 10:
#         return None


# async def main():
#     async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
#         await asyncio.gather(
#             *[screen_liquidity(df_index, session) for df_index in range(0, len(df))]
#         )

asyncio.run(main())
