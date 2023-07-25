import requests
import pandas as pd
import json
from requests.exceptions import Timeout
from helper_functions import print_status, create_outfile

# print header message to terminal
process_name = "NASDAQ Listings"
process_stage = 0
print_status(process_name, process_stage, True)

# request nasdaq listing data
url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
}

# extract symbols from response
try:
    response = requests.get(url, headers=headers, timeout=15)
except Timeout:
    print(
        "Failed to download stock-list from NASDAQ (are you connected to the internet?)"
    )
    raise SystemExit

response_dict = json.loads(response.content.decode())
rows = response_dict["data"]["rows"]
df = pd.DataFrame.from_dict(rows)
df = df.drop(
    columns=[
        "sector",
        "url",
        "lastsale",
        "netchange",
        "pctchange",
        "volume",
        "country",
        "ipoyear",
    ]
)
df.columns = ["Symbol", "Company Name", "Market Cap", "Industry"]

# remove any symbols containing a '/' or '^'
df = df[~(df["Symbol"].str.contains("/") | df["Symbol"].str.contains("\^"))]

# serialize data in JSON format and save on machine
create_outfile(df, "nasdaq_listings")

# print footer message to terminal
print(f"{len(df)} symbols extracted.")
print_status(process_name, process_stage, False)
