import yfinance as yf
import os
import json
import pandas as pd
import datetime as dt
from helper_functions import relative_strength, print_status

# print header message to terminal
process_name = "Relative Strength"
process_stage = 1
print_status(process_name, process_stage, True)

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

tickers = yf.download(temp_symbol_list, period="1y", interval="1d", timeout=10)
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

    # calculate raw relative strength using the following formula:
    # RS = 0.2(Q1 %Δ) + 0.2(Q2 %Δ) + 0.2(Q3 %Δ) + 0.4(Q4 %Δ)
    q1_start = col.iloc[0]
    q1_end = col.iloc[62]

    q2_start = col.iloc[63]
    q2_end = col.iloc[125]

    q3_start = col.iloc[126]
    q3_end = col.iloc[188]

    q4_start = col.iloc[189]
    q4_end = col.iloc[250]

    rs_raw = relative_strength(
        q1_start, q1_end, q2_start, q2_end, q3_start, q3_end, q4_start, q4_end
    )

    print(
        """Symbol: {} | Relative Strength (raw): {:.3f}
        Q1 : start: ${:.2f}, end: ${:.2f}
        Q2 : start: ${:.2f}, end: ${:.2f}
        Q3 : start: ${:.2f}, end: ${:.2f}
        Q4 : start: ${:.2f}, end: ${:.2f}\n""".format(
            symbol,
            rs_raw,
            q1_start,
            q1_end,
            q2_start,
            q2_end,
            q3_start,
            q3_end,
            q4_start,
            q4_end,
        )
    )

    symbols.append(symbol)
    rs_raws.append(rs_raw)

# print footer message to terminal
print("x symbols passed")
print("Failed Symbols: {}".format(", ".join(failed)))
print_status(process_name, process_stage, False)
