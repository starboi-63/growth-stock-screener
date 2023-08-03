import requests

# constants
header = {"User-Agent": "name@domain.com"}


def get_cik(symbol: str) -> str:
    conversions = requests.get(
        "https://www.sec.gov/files/company_tickers.json", headers=header
    )

    return conversions


print(get_cik("NVDA"))
