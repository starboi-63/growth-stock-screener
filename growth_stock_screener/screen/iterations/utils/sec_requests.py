import requests
from requests.exceptions import JSONDecodeError
import pandas as pd
from typing import List, Dict
from tqdm import tqdm
from datetime import datetime
import asyncio
import aiohttp
from aiohttp.client import ClientSession
from .scraping import get

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


async def get_company_facts(symbol: str, session: ClientSession) -> dict:
    """Request all available concept data for a stock symbol from SEC.gov"""
    # construct url for request to SEC's API
    cik = get_cik(symbol)

    if cik is None:
        return None

    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"

    try:
        response = await get(url, session, headers=header)
        company_facts = response.json()["facts"]

        if "us-gaap" not in company_facts:
            return {"Foreign Stock": True}

        return company_facts["us-gaap"]
    except Exception:
        return None


async def fetch_revenues(symbol: str, session: ClientSession) -> pd.DataFrame:
    """Fetch quarterly revenue data for a stock symbol from SEC filings."""
    # get all available SEC data on company
    data = await get_company_facts(symbol, session)

    if data is None:
        return None

    if "Foreign Stock" in data:
        return pd.DataFrame.from_dict([data])

    # different companies file revenue with varying concepts, and we must check which concept has the most up-to-date data
    revenue_concepts = [
        "Revenues",
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "RevenueFromContractWithCustomerIncludingAssessedTax",
        "RevenuesNetOfInterestExpense",
        "RevenuesExcludingInterestAndDividends",
        "RegulatedAndUnregulatedOperatingRevenue",
        "InterestAndDividendIncomeOperating",
    ]
    revenue_concept_data = []

    # add available revenue concept dictionaries to list
    for concept in revenue_concepts:
        if concept in data:
            try:
                rows = data[concept]["units"]["USD"]

                # check for foreign stocks
                if (len(rows) > 0) and (rows[0]["form"] == "20-F"):
                    return pd.DataFrame.from_dict([{"Foreign Stock": True}])

                revenue_concept_data.append(rows)
            except KeyError:
                continue

    # determine which revenue concept dictionary to use for revenue data
    revenue_data = find_most_updated(revenue_concept_data)

    if revenue_data is None:
        return None

    # convert dictionary to pandas DataFrame and remove listings which don't have specified timeframes
    revenue_df = pd.DataFrame.from_dict(revenue_data)
    revenue_df = revenue_df[~pd.isna(revenue_df["frame"])]

    return revenue_df


def find_most_updated(dicts: List[List[Dict]]) -> List[Dict]:
    """Return the SEC revenue concept which contains the most up-to-date information."""
    if len(dicts) == 0:
        return None

    # populate lists with the most recent end-dates and listings present in the concept dictionary
    last_dates = []
    listing_counts = []

    for dict in dicts:
        last_row = dict[-1]
        last_date = last_row["end"]
        date = datetime.strptime(last_date, "%Y-%m-%d").date()
        last_dates.append(date)
        listing_counts.append(len(dict))

    # determine the index of the concept dictionary with the most recent listing
    # if multiple revenue concepts are equally up-to-date, choose the concept with the most listings
    most_recent_date = max(last_dates)
    most_updated_indices = [
        i for i in range(len(last_dates)) if last_dates[i] == most_recent_date
    ]
    most_updated_index = max(most_updated_indices, key=lambda i: listing_counts[i])

    return dicts[most_updated_index]


def fetch_revenues_bulk(symbols: List[str]) -> Dict[str, pd.DataFrame]:
    """Fetch quarterly revenue data for multiple stock symbols from SEC filings."""

    async def helper(symbols: List[str]) -> Dict[str, pd.DataFrame]:
        ret = {}

        print("Fetching revenue data . . .\n")

        for symbol in tqdm(symbols):
            ret[symbol] = fetch_revenues(symbol)

        return ret

    return helper(symbols)


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
