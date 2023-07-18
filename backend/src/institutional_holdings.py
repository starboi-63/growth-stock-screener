from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# construct the url and headers for the request
symbol = "AAPL"

url = "https://www.nasdaq.com/market-activity/stocks/{}/institutional-holdings".format(
    symbol
)

user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
)

# configure selenium to use a headless chrome browser instance
options = webdriver.ChromeOptions()
options.add_argument("no-sandbox")
options.add_argument("headless")
options.add_argument("disable-gpu")
options.add_argument("user-agent={}".format(user_agent))

driver = webdriver.Chrome(options=options)
driver.get(url)

print(driver.page_source)
