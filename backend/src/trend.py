from helper_functions import *
import asyncio
import aiohttp
from tqdm.asyncio import tqdm_asyncio

# print header message to terminal
process_name = "Trend"
process_stage = 3
print_status(process_name, process_stage, True)

# retreive JSON data from previous screen iteration
df = open_outfile("liquidity")
