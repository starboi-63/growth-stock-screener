import yfinance as yf
import os
import json
import pandas as pd

# open json data extracted from nasdaq as pandas dataframe
json_path = os.path.join(os.getcwd(), "backend", "json", "nasdaq_listings.json")
df = pd.read_json(json_path, orient="index")
df.columns = ["Symbol"]

print(df)
