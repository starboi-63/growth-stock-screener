import pandas as pd
from typing import Dict
from utils.logs import *
from utils.outfiles import *
from utils.sec_requests import *
from utils.calculations import *

# constants
min_growth_percent = 25

# print header message to terminal
process_name = "Revenue Growth"
process_stage = 4
print_status(process_name, process_stage, True)
print(f"Minimum quarterly revenue growth to pass: {min_growth_percent}%\n")

# logging data (printed to console after screen finishes)
logs = []

# retreive JSON data from previous screen iteration
df = open_outfile("trend")

# populate these lists while iterating through symbols
successful_symbols = []
failed_symbols = []

# fetch revenue data for all symbols
symbol_list = list(df["Symbol"])
symbol_list = [df.iloc[10]["Symbol"]]
revenue_data = fetch_revenues_bulk(symbol_list)


def revenue_growth(timeframe: str, df: pd.DataFrame) -> float:
    """Calculate the revenue growth for the given timeframe compared to the same timeframe one year earlier."""
    prev_timeframe = previous_timeframe(timeframe)

    revenue = extract_revenue(timeframe, df)
    prev_revenue = extract_revenue(prev_timeframe, df)

    if (revenue is None) or (prev_revenue is None):
        return None

    return percent_change(prev_revenue, revenue)


def extract_comparison_revenues(symbol: str) -> Dict[str, Dict[str, float]]:
    """Extract revenue from the two most recent financial quarters and their corresponding quarters one year ago."""
    revenue_df = revenue_data[symbol]

    q1_row = revenue_df.iloc[-2] if (len(revenue_df) >= 2) else None
    q2_row = revenue_df.iloc[-1] if (len(revenue_df) >= 1) else None

    q1_timeframe = q1_row["frame"] if (q1_row is not None) else None
    q2_timeframe = q2_row["frame"] if (q2_row is not None) else None

    return None


def screen_revenue_growth(df_index: int) -> None:
    """Populate stock data lists based on whether the given dataframe row has strong revenue growth."""
    row = df.iloc[df_index]

    symbol = row["Symbol"]
    rs = row["RS"]
    revenue_data = extract_comparison_revenues(symbol)

    # # handle null values from unsuccessful fetching
    # if revenue_data is None:
    #     logs.append(skip_message(symbol, "insufficient data"))
    #     failed_symbols.append(symbol)
    #     return

    # q1_revenue_growth = 5
    # q2_revenue_growth = 5

    # # print revenue growth data to console
    # if "Q2" in revenue_data:
    #     logs.append(
    #         f"""\n{symbol} | Q1 revenue growth: {q1_revenue_growth:.0f}%, Q2 revenue growth: {q2_revenue_growth:.0f}%, RS: {rs}
    #         Q1 : current revenue: ${revenue_data["Q1"]["Current"]:.0f}M, previous revenue: ${revenue_data["Q1"]["Previous"]:.0f}M
    #         Q2 : current revenue: ${revenue_data["Q2"]["Current"]:.0f}M, previous revenue: ${revenue_data["Q2"]["Previous"]:.0f}M\n"""
    #     )
    # else:
    #     logs.append(
    #         f"""\n{symbol} | Q1 revenue growth: {q1_revenue_growth:.0f}%, RS: {rs}
    #         Q1 : current revenue: ${revenue_data["Q1"]["Current"]:.0f}M, previous revenue: ${revenue_data["Q1"]["Previous"]:.0f}M\n"""
    #     )

    # # filter out stocks with low quarterly revenue growth
    # if (q1_revenue_growth < min_growth_percent) and (rs < 99):
    #     logs.append(filter_message(symbol))
    #     return

    # if (
    #     (q2_revenue_growth is not None)
    #     and (q2_revenue_growth < min_growth_percent)
    #     and (rs < 99)
    # ):
    #     logs.append(filter_message(symbol))
    #     return

    successful_symbols.append(
        {
            "Symbol": symbol,
            "Company Name": row["Company Name"],
            "Industry": row["Industry"],
            "RS": rs,
            "Price": row["Price"],
            "Market Cap": row["Market Cap"],
            # "Revenue Growth % (most recent Q)": q2_revenue_growth,
            # "Revenue Growth % (previous Q)": q1_revenue_growth,
            "50-day Average Volume": row["50-day Average Volume"],
            "% Below 52-week High": row["% Below 52-week High"],
        }
    )


screen_revenue_growth(10)

# create a new dataframe with symbols which satisfied revenue_growth criteria
screened_df = pd.DataFrame(successful_symbols)

# serialize data in JSON format and save on machine
create_outfile(screened_df, "revenue_growth")

# print log
print("".join(logs))

# print footer message to terminal
print(f"{len(failed_symbols)} symbols failed (insufficient revenue reports).")
print(
    f"{len(df) - len(screened_df) - len(failed_symbols)} symbols filtered (revenue growth too low)."
)
print(f"{len(screened_df)} symbols passed.")
print_status(process_name, process_stage, False)
