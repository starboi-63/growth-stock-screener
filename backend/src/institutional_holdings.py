from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# construct the url and headers for the request
symbol = "AAPL"
url = f"https://www.nasdaq.com/market-activity/stocks/{symbol}/institutional-holdings"
user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
)

# configure selenium to use a headless chrome browser instance to request data
options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("disable-gpu")
options.add_argument(f"user-agent={user_agent}")

driver = webdriver.Chrome(options=options)
driver.get(url)

# extract institutional holdings information from site HTML
soup = BeautifulSoup(driver.page_source, "html.parser")

holdings_table_rows = soup.find_all("tr", class_="institutional-holdings__row")

for row in holdings_table_rows:
    print(row)
