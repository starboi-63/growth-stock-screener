import requests
import pandas as pd
import json
import os

# request nasdaq listing data
url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
}

# extract symbols from response
response = requests.get(url, headers=headers, timeout=15)
response_dict = json.loads(response.content.decode())
rows = response_dict["data"]["rows"]
df = pd.DataFrame.from_dict(rows)
df = df["symbol"]

# serialize data in JSON format and save on machine
serialized_json = df.to_json()
outfile_name = "nasdaq_listings.json"
outfile_path = os.path.join(os.getcwd(), "backend", "json", outfile_name)

with open(outfile_path, "w") as outfile:
    outfile.write(serialized_json)
