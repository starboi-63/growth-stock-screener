from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

# constants
timeout = 10
holdings_data_xpath = "/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div[2]/div/div[2]/div/table/tbody"

# construct the url and headers for the request
symbol = "IONQ"
url = f"https://www.nasdaq.com/market-activity/stocks/{symbol}/institutional-holdings"
user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
)

# configure selenium to use a headless chrome browser instance to request data
options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("disable-gpu")
options.add_argument(f"user-agent={user_agent}")
options.page_load_strategy = "none"
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

# perform GET request
driver.get(url)

# load page until holdings table is present in the DOM
try:
    data_present = EC.presence_of_element_located((By.XPATH, holdings_data_xpath))
    WebDriverWait(driver, timeout).until(data_present)
    driver.execute_script("window.stop();")
except TimeoutException:
    print(f"Skipping {symbol} (request timed out)")
    # continue

# extract institutional holdings information from site HTML
soup = BeautifulSoup(driver.page_source, "html.parser")

# the second table on the "institutional-holdings" page has position data
holdings_tables = soup.find_all("tbody", class_="institutional-holdings__body")
active_positions_table = holdings_tables[1]

# extract the number of institutions that have increased or decreased positions
table_rows = list(active_positions_table.children)
increased_row = list(table_rows[0].contents)
decreased_row = list(table_rows[1].contents)

increased_positions = increased_row[1].contents[0]
increased_shares = increased_row[2].contents[0]
decreased_positions = decreased_row[1].contents[0]
decreased_shares = decreased_row[2].contents[0]

# print extracted data to terminal
print(
    f"""Symbol: {symbol}
    Increased Positions: {increased_positions} | Increased Shares: {increased_shares}
    Decreased Positions: {decreased_positions} | Decreased Shares: {decreased_shares}"""
)

# close all chrome browser instances
driver.quit()
