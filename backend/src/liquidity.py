import requests
import pandas

symbol = "NVDA"
url = f"https://www.barchart.com/stocks/quotes/{symbol}/technical-analysis"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
}

try:
    response = requests.get(url, headers=headers, timeout=15)
except TimeoutError:
    print(f"Skipping {symbol} (request timed out) . . .")

print(response.content)
