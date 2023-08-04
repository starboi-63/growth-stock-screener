import requests
from requests.exceptions import JSONDecodeError
import pandas as pd
import json

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
    return conversions_df.loc[symbol]["cik_str"]


def get_concept(symbol: str, concept: str) -> dict:
    """Request concept data for a stock symbol from SEC.gov."""
    # cik's are left-padded with zeroes to a length of 10 characters
    cik = str(get_cik(symbol)).zfill(10)
    url = (
        f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/{concept}.json"
    )

    try:
        response = requests.get(url, headers=header)
        return response.json()
    except JSONDecodeError:
        return None


def get_revenues(symbol: str) -> pd.DataFrame:
    # different companies file revenue with various concepts, and we must check which has the most data
    revenue_concepts = [
        "Revenues",
        "RevenueFromContractWithCustomerExcludingAssessedTax",
    ]

    concept_data = []

    # iterate over concepts and append data to list if available
    for concept in revenue_concepts:
        data = get_concept(symbol, concept)
        concept_data.append(data["units"]["USD"] if (data is not None) else {})

    # store the longest dictionary as the final source of revenue data
    revenue_data = max(concept_data, key=len)

    # convert dictionary to pandas DataFrame and remove listings which don't have specified timeframes
    revenue_df = pd.DataFrame.from_dict(revenue_data)
    revenue_df = revenue_df[~pd.isna(revenue_df["frame"])]

    return revenue_df


print(get_revenues("AI"))
