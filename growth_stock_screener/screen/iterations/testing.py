import yfinance as yf
import pandas as pd
from typing import List
import pandas as pd
import os


def open_outfile(filename: str) -> pd.DataFrame:
    """Open json outfile data as pandas dataframe."""
    json_path = os.path.join(
        os.getcwd(), "growth_stock_screener", "json", f"{filename}.json"
    )
    df = pd.read_json(json_path)
    return df


# open json data extracted from nasdaq as pandas dataframe
df = open_outfile("nasdaq_listings")

# extract symbols from dataframe
symbol_list = df["Symbol"].values.tolist()
symbol_list = [symbol_list[i] for i in range(100)]

# download all historical price data at once


def yf_download_batches(
    batch_size: int, symbol_list: List[str], timeout: int
) -> pd.DataFrame:
    def download_batch(start: int, end: int) -> pd.DataFrame:
        print(
            f"Batch {batch_number}: Symbols {start + 1} to {end} ({symbol_list[start]}—{symbol_list[end - 1]})"
        )
        batch = yf.download(
            [symbol_list[i] for i in range(start, end)], period="2y", timeout=timeout
        )
        print()
        return batch

    print("Fetching historical price data . . .\n")
    dfs = []
    start = 0
    end = min(batch_size, len(symbol_list))
    batch_number = 1

    # loop-and-a-half
    while end < len(symbol_list):
        dfs.append(download_batch(start, end))

        # increment counters
        start += batch_size
        end = min(end + batch_size, len(symbol_list))
        batch_number += 1

    dfs.append(download_batch(start, end))

    print(dfs)


yf_download_batches(33, symbol_list, 30)
