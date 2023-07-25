from helper_functions import *
import asyncio
import aiohttp
from tqdm.asyncio import tqdm_asyncio

# print header message to terminal
process_name = "Trend"
process_stage = 3
print_status(process_name, process_stage, True)

# logging data (printed to console after screen finishes)
logs = []

# retreive JSON data from previous screen iteration
df = open_outfile("liquidity")

# populate these lists while iterating through symbols
successful_symbols = []
failed_symbols = []


async def fetch(symbol: str, session):
    """coroutine for get request to movingaverages.com using a stock symbol"""
    url = f"https://www.movingaverages.com/pivot-points/{symbol}"

    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        logs.append(skip_message(symbol, e))
        failed_symbols.append(e)
        return None


async def main():
    async with aiohttp.ClientSession() as session:
        response = await fetch("NVDA", session)
        print(response)


asyncio.run(main())
