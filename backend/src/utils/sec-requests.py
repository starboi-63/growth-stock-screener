import requests
from requests.exceptions import JSONDecodeError
import pandas as pd

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
    """Fetch quarterly revenue data for a stock symbol from SEC filings."""
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


def revenue_growth(frame: str, df: pd.DataFrame) -> float:
    frame_components = frame.split("Q")
    year = frame_components[0].replace("CY", "")
    quarter = None if (len(frame_components) < 2) else frame_components[1]

    if quarter is None:
        # must convert annual revenue to quarterly revenue by subtracting previous three quarters
        try:
            revenue = subtract_prev_quarters(frame, df)
            print(revenue)
        except Exception:
            return None

    return None


def subtract_prev_quarters(frame: str, df: pd.DataFrame) -> float:
    """Convert annual revenue to quarterly revenue by subtracting revenue from the previous three 10-Q SEC filings."""
    index = df.index.get_loc(df.index[df["frame"] == frame][0])
    quarter_indices = [index - 3, index - 2, index - 1, index]
    revenues = []

    if quarter_indices[0] < 0:
        return None

    for i in quarter_indices:
        row = df.iloc[i]

        if (i < index) and ("Q" not in row["frame"]):
            return None

        revenues.append(row["val"])

    revenue = revenues[3] - (revenues[0] + revenues[1] + revenues[2])
    return revenue


df = get_revenues("AAPL")
print(df)
print()
print(revenue_growth("CY2022", df))
