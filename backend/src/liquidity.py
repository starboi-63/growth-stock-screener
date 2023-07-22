import requests
from requests.exceptions import Timeout
import pandas as pd
import json
import os
import asyncio

# retreive JSON data from previous screen iteration
json_path = os.path.join(os.getcwd(), "backend", "json", "relative_strengths.json")
df = pd.read_json(json_path)

# extract columns from dataframe
symbol_list = df["Symbol"].values.tolist()


# symbol = "NVDA"
# url = f"https://www.barchart.com/stocks/quotes/{symbol}/technical-analysis"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
# }


# print(f"Skipping {symbol} (request timed out) . . .")
