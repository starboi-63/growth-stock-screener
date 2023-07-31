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


async def fetch_revenues(symbol: str, session: ClientSession) -> Dict[str, float]:


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        print(await get("NVDA", session))


asyncio.run(main())
