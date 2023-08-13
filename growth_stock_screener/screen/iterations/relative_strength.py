import yfinance as yf
import pandas as pd
from termcolor import colored, cprint
from .utils import *
from ..settings import min_rs

# constants
timeout = 30

# print header message to terminal
process_name = "Relative Strength"
process_stage = 1
print_status(process_name, process_stage, True)
print_minimums({"RS rating": min_rs})

# logging data (printed to console after screen finishes)
logs = []

# open json data extracted from nasdaq as pandas dataframe
df = open_outfile("nasdaq_listings")
df_index = 0

# extract symbols from dataframe
symbol_list = df["Symbol"].values.tolist()

# download all historical price data at once
print("Fetching historical price data . . .\n")
tickers = yf.download(symbol_list, period="2y", timeout=timeout)
price_df = tickers["Adj Close"]

# populate these lists while iterating through symbols
successful_symbols = []
failed_symbols = []

# add empty line
print()

for symbol in price_df:
    col = price_df[symbol]
    end_index = len(col) - 1

    # eliminate symbol if it has not traded for 1yr
    first_valid_index = 0

    for i in range(len(col)):
        if not pd.isna(col[i]):
            first_valid_index = i
            break

    if (end_index < 251) or ((end_index - first_valid_index + 1) < 252):
        logs.append(skip_message(symbol, "stock has not traded long enough"))
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
        logs.append(skip_message(symbol, "insufficient data"))
        failed_symbols.append(symbol)
        continue

    rs_raw = relative_strength(
        q1_start, q1_end, q2_start, q2_end, q3_start, q3_end, q4_start, q4_end
    )

    logs.append(
        f"""\n{symbol} | Relative Strength (raw): {rs_raw:.3f}
        Q1 : start: ${q1_start:.2f}, end: ${q1_end:.2f}
        Q2 : start: ${q2_start:.2f}, end: ${q2_end:.2f}
        Q3 : start: ${q3_start:.2f}, end: ${q3_end:.2f}
        Q4 : start: ${q4_start:.2f}, end: ${q4_end:.2f}\n"""
    )

    while df.iloc[df_index]["Symbol"] != symbol:
        df_index += 1

    row = df.iloc[df_index]

    successful_symbols.append(
        {
            "Symbol": symbol,
            "Company Name": row["Company Name"],
            "Market Cap": row["Market Cap"],
            "Industry": row["Industry"],
            "Price": q4_end,
            "RS (raw)": rs_raw,
        }
    )

# create a new dataframe with symbols whose relative strengths were successfully calculated
rs_df = pd.DataFrame(successful_symbols)

# calculate RS rankings and filter out any symbols with an RS below the specified minimum
rs_df["RS"] = rs_df["RS (raw)"].rank(pct=True)
rs_df["RS"] = rs_df["RS"].map(lambda rs: round(100 * rs))
rs_df = rs_df.drop(columns=["RS (raw)"])
rs_df = rs_df[rs_df["RS"] >= min_rs]

# serialize data in JSON format and save on machine
create_outfile(rs_df, "relative_strengths")

# print log
print("".join(logs))

# print footer message to terminal
cprint(f"{len(failed_symbols)} symbols failed (insufficient data).", "dark_grey")
cprint(
    f"{len(symbol_list) - len(rs_df) - len(failed_symbols)} symbols filtered (RS below {min_rs} or stock too young).",
    "dark_grey",
)
cprint(f"{len(rs_df)} symbols passed.", "green")
print_status(process_name, process_stage, False)
print_divider()
