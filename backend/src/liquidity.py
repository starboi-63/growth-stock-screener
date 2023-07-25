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

    symbol = row["Symbol"]
    name = row["Company Name"]
    price = row["Price"]
    market_cap = row["Market Cap"]
    volume = extract_avg_volume(await get_response(symbol, session))
    industry = row["Industry"]
    rs = row["RS"]

    # check if null values are present in screen criteria
    if pd.isna(market_cap) or volume is None:
        failed_symbols.append(symbol)
        return

    # filter out stocks with a market cap below $1B, a price below $10, or a 50-day average volume below 100,000 shares
    if market_cap < 1000000000 or price < 10 or volume < 100000:
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
        await asyncio.gather(
            *[screen_liquidity(df_index, session) for df_index in range(0, len(df))]
        )


asyncio.run(main())

print(successful_symbols)
