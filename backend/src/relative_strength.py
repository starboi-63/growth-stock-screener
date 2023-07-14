import yfinance as yf
import os
import json
import pandas as pd
import datetime as dt

# open json data extracted from nasdaq as pandas dataframe
json_path = os.path.join(os.getcwd(), "backend", "json", "nasdaq_listings.json")
df = pd.read_json(json_path, orient="index")
df.columns = ["Symbol"]

symbol_list = df["Symbol"].values.tolist()
temp_symbol_list = [
    "NVDA",
    "PLTR",
    "AI",
    "SLRN",
    "ATMU",
    "BAD/TKR",
    "MDB",
    "INTC",
    "IBM",
    "CRWD",
    "ELF",
    "SNOW",
    "TWLO",
    "SDGR",
    "ASML",
    "ACLS",
]

tickers = yf.download(temp_symbol_list, period="1y")
price_df = tickers["Adj Close"]

symbols = []
rs_raws = []
failed = []

for symbol in price_df:
    col = price_df[symbol]

    # eliminate ticker if stock has not traded for at least 1yr
    if pd.isna(col.iloc[0]) or pd.isna(col.iloc[len(price_df) - 1]):
        failed.append(symbol)
        continue

    # calculate raw relative strength
    price_12mo = col.iloc[0]
    price_9mo = col.iloc[62]
    price_6mo = col.iloc[125]
    price_3mo = col.iloc[188]
    price_cur = col.iloc[250]

    print(
        "Symbol:{} | 12mo:{} 9mo:{} 6mo:{} 3mo:{} cur:{}".format(
            symbol, price_12mo, price_9mo, price_6mo, price_3mo, price_cur
        )
    )

    symbols.append(symbol)

print(failed)
print(symbols)
