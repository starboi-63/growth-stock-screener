import requests
import pandas as pd
import json

url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
}

response = requests.get(url, headers=headers, timeout=15)
response_dict = json.loads(response.content.decode())

rows = response_dict["data"]["rows"]
df = pd.DataFrame.from_dict(rows)

print(df["symbol"])
