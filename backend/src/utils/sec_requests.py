import requests
from requests.exceptions import JSONDecodeError
import pandas as pd
from typing import List, Dict
import time
from tqdm import tqdm
from datetime import datetime

# constants
header = {"User-Agent": "name@domain.com"}

# get table to convert from stock tickers to cik's
response = requests.get(
    "https://www.sec.gov/files/company_tickers.json", headers=header
)
conversions_df = pd.DataFrame.from_dict(response.json(), orient="index").set_index(
    "ticker"
)


def get_cik(symbol: str) -> str:
    """Convert a stock symbol into a cik used by the SEC for corporate filings."""
    try:
        cik = conversions_df.loc[symbol]["cik_str"]
        cik_padded = str(cik).zfill(10)
        return cik_padded
    except KeyError:
        return None


def get_concept(symbol: str, concept: str) -> dict:
    """Request concept data for a stock symbol from SEC.gov."""
    # construct url for request to SEC's API
    cik = get_cik(symbol)

    if cik is None:
        return None

    url = (
        f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/{concept}.json"
    )

    try:
        response = requests.get(url, headers=header)
        return response.json()
    except JSONDecodeError:
        return None


def get_company_facts(symbol: str) -> dict:
    """Request all available concept data for a stock symbol from SEC.gov"""
    # construct url for request to SEC's API
    cik = get_cik(symbol)

    if cik is None:
        return None

    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"

    try:
        response = requests.get(url, headers=header)
        return response.json()
    except JSONDecodeError:
        return None


def fetch_revenues(symbol: str) -> pd.DataFrame:
    """Fetch quarterly revenue data for a stock symbol from SEC filings."""
    # different companies file revenue with various concepts, and we must check which has the most up-to-date data
    revenue_concepts = [
        "Revenues",
        "RevenueFromContractWithCustomerIncludingAssessedTax",
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "RevenuesNetOfInterestExpense",
        "SalesRevenueNet",
        "RevenuesExcludingInterestAndDividends",
    ]

    concept_data = []

    return None

    # # iterate over concepts and append data to list if available
    # for concept in revenue_concepts:
    #     data = get_concept(symbol, concept)

    #     if data is not None:
    #         concept_data.append(data["units"]["USD"])

    # # store the dictionary with the most recent listings as the final source of revenue data
    # revenue_data = find_most_updated(concept_data)
    # # if revenue_data == {}:
    # #     return None

    # # convert dictionary to pandas DataFrame and remove listings which don't have specified timeframes
    # revenue_df = pd.DataFrame.from_dict(revenue_data)
    # revenue_df = revenue_df[~pd.isna(revenue_df["frame"])]

    # return revenue_df


def find_most_updated(dicts: List[Dict]) -> Dict:
    if len(dicts) == 0:
        return None

    largest_date = dicts[0].values()[-1]


def fetch_revenues_bulk(symbols: List[str]) -> Dict[str, pd.DataFrame]:
    """Fetch quarterly revenue data for multiple stock symbols from SEC filings."""
    ret = {}

    print("Fetching revenue data . . .\n")

    for symbol in tqdm(symbols):
        ret[symbol] = fetch_revenues(symbol)
        # SEC sets maximum API usage rate to 10 calls/sec
        time.sleep(0.1)

    return ret


def subtract_prev_quarters(timeframe: str, df: pd.DataFrame) -> float:
    """Convert annual revenue to quarterly revenue by subtracting revenue from the previous three 10-Q SEC filings."""
    # determine the index of the row with revenue for the inputted timeframe
    try:
        index = df.index.get_loc(df.index[df["frame"] == timeframe][0])
    except IndexError:
        return None

    quarter_indices = [index - 3, index - 2, index - 1, index]
    revenues = []

    # ensure that there are enough filings to perform subtraction
    if quarter_indices[0] < 0:
        return None

    # extract revenues for each index
    for i in quarter_indices:
        row = df.iloc[i]

        if (i < index) and ("Q" not in row["frame"]):
            return None

        revenues.append(float(row["val"]))

    # subtract quarterly revenues from annual revenue
    revenue = revenues[3] - (revenues[0] + revenues[1] + revenues[2])
    return revenue


def extract_revenue(timeframe: str, df: pd.DataFrame) -> float:
    """Return the revenue for a given timeframe from an SEC revenue DataFrame."""
    if "Q" in timeframe:
        # search DataFrame for quarterly timeframe
        try:
            row = df[df["frame"] == timeframe].iloc[0]
            value = row["val"]
            return float(value)
        except IndexError:
            return None
    else:
        # convert annual revenue into quarterly revenue
        return subtract_prev_quarters(timeframe, df)


def previous_timeframe(timeframe: str) -> str:
    """Return an SEC timeframe that is 1 year earlier than the inputted timeframe."""
    year = int(timeframe[2:6]) - 1
    quarter = timeframe[6:]
    return f"CY{year}{quarter}"
