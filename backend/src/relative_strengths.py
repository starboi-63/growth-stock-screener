import yfinance as yf
import os
import json
import pandas as pd
import datetime as dt
from helper_functions import relative_strength, print_status

# minimum RS required to pass this screen
min_rs = 90

# print header message to terminal
process_name = "Relative Strength"
process_stage = 1
print_status(process_name, process_stage, True)
print("Minimum Relative Strength to Pass: {}".format(min_rs))

# open json data extracted from nasdaq as pandas dataframe
json_path = os.path.join(os.getcwd(), "backend", "json", "nasdaq_listings.json")
df = pd.read_json(json_path, orient="index")
df.columns = ["Symbol"]

# extract symbols from dataframe
symbol_list = df["Symbol"].values.tolist()

# download all historical price data at once
tickers = yf.download(symbol_list, period="2y", timeout=10)
price_df = tickers["Adj Close"]

# populate these lists while iterating through symbols
successful_symbols = []
rs_raws = []
failed_symbols = []

# add empty line
print()

for symbol in price_df:
    col = price_df[symbol]
    end_index = len(col) - 1

    # eliminate symbol if it has not traded for 1yr
    if end_index < 251:
        failed_symbols.append(symbol)
        continue

    # calculate raw relative strength using the following formula:
    # RS = 0.2(Q1 %Δ) + 0.2(Q2 %Δ) + 0.2(Q3 %Δ) + 0.4(Q4 %Δ)
    q1_start = col.iloc[end_index - 251]  # day 1
    q1_end = col.iloc[end_index - 189]  # day 63

    q2_start = col.iloc[end_index - 188]  # day 64
    q2_end = col.iloc[end_index - 126]  # day 126

    q3_start = col.iloc[end_index - 125]  # day 127
    q3_end = col.iloc[end_index - 63]  # day 189

    q4_start = col.iloc[end_index - 62]  # day 190
    q4_end = col.iloc[end_index]  # day 252

    # eliminate symbol if nan values are present
    if (
        pd.isna(q1_start)
        or pd.isna(q1_end)
        or pd.isna(q2_start)
        or pd.isna(q2_end)
        or pd.isna(q3_start)
        or pd.isna(q3_end)
        or pd.isna(q4_start)
        or pd.isna(q4_end)
    ):
        failed_symbols.append(symbol)
        continue

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

    successful_symbols.append(symbol)
    rs_raws.append(rs_raw)

# create a new dataframe with symbols whose relative strengths were successfully calculated
rs_df = pd.DataFrame(
    list(zip(successful_symbols, rs_raws)), columns=["Symbol", "RS (raw)"]
)

rs_df["RS"] = rs_df["RS (raw)"].rank(pct=True)
rs_df["RS"] = rs_df["RS"].map(lambda rs: round(100 * rs))
rs_df = rs_df.drop(columns=["RS (raw)"])
rs_df = rs_df[rs_df["RS"] >= min_rs]

# serialize data in JSON format and save on machine
serialized_json = rs_df.to_json()
outfile_name = "relative_strengths.json"
outfile_path = os.path.join(os.getcwd(), "backend", "json", outfile_name)

with open(outfile_path, "w") as outfile:
    outfile.write(serialized_json)

# print footer message to terminal
print("{} symbols failed (insufficient data).".format(len(failed_symbols)))
print(
    "{} symbols filtered (RS below {}).".format(
        len(symbol_list) - len(rs_df) - len(failed_symbols), min_rs
    )
)
print("{} symbols passed.".format(len(rs_df)))
print_status(process_name, process_stage, False)
