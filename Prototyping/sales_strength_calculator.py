import pandas
import requests
import math
import sys
import os
import time
import screen

os.system("color")

# set to true if extra information or full responses are desired (ex. for debugging)
show_extra_information = True
show_responses = False


def percent_change(initial, final):
    return (final - initial) / initial * 100.0


def print_countdown():
    for j in range(61, 0, -1):
        time.sleep(1)
        sys.stdout.write("Waiting " + str(j) + " seconds ")
        sys.stdout.write("\033[19D" if j - 1 / 10 >= 1 else "\033[18D")  # move cursor left
        sys.stdout.flush()


symbol_list = pandas.read_excel("results/Stage 2.xlsx")['Symbol']

used_symbols = []
sales_strength_array = []

n = 0
request_count = 0
for symbol in symbol_list:
    n += 1

    # AVOIDING REQUEST LIMIT

    # Polygon limits free users to 5 API requests per minute
    if request_count != 0 and request_count % 5 == 0:
        print_countdown()

    # DATA COLLECTION

    # the url and parameters for get request to polygon's API
    url = f"https://api.polygon.io/vX/reference/financials"

    # the number of quarters / years of data to request
    quarter_limit = 15
    year_limit = 5

    parameters = \
        {
            'ticker': symbol,
            'apiKey': 'l_OMHP9XcH_CvW_1PPl0RWVdb61xD1K6',
            'timeframe': 'quarterly',
            'limit': quarter_limit
        }

    # response containing data from 10-Q filings
    request_count += 1
    try:
        quarterly_filings = requests.get(url, parameters).json()['results']
    except:
        print(f"Skipping {symbol} (request failed)")
        continue

    if request_count % 5 == 0:
        print_countdown()

    parameters = \
        {
            'ticker': symbol,
            'apiKey': 'l_OMHP9XcH_CvW_1PPl0RWVdb61xD1K6',
            'timeframe': 'annual',
            'limit': year_limit
        }

    # response containing data from 10-K filings
    request_count += 1
    try:
        annual_filings = requests.get(url, parameters).json()['results']
    except:
        print(f"Skipping {symbol} (request failed)")
        continue

    # combine quarterly and full year reports into one array
    all_filings = []

    # combine 10-Q and 10-K filings into one array in order of period end date
    for quarter in quarterly_filings:
        all_filings.append(quarter)

    for year in annual_filings:
        all_filings.append(year)

    all_filings.sort(key = lambda x: x['end_date'], reverse = True)

    # isolate quarterly and annual sales from each filing for use in calculations
    quarterly_sales = []
    annual_sales = []

    for i in range(0, len(all_filings)):
        current_filing = all_filings[i]
        income_statement = current_filing['financials']['income_statement']

        end_date = current_filing['end_date']
        year = current_filing['fiscal_year']
        period = current_filing['fiscal_period']
        # sales data might be unavailable for some ticker symbols
        try:
            sales = income_statement['revenues']['value']
            sales_label = income_statement['revenues']['label']
        except KeyError:
            sales = math.nan
            sales_label = 'unavailable'

        # if the filing is for the fiscal year end (ie. 10-K), the sales from the past three quarters is subtracted from the annual sales, isolating fourth quarter sales
        if period == "FY":
            annual_sales.append([symbol, end_date, year, period, sales_label, sales])

            if i < len(all_filings) - 3:
                try:
                    q3_ytd_sales = all_filings[i + 1]['financials']['income_statement']['revenues']['value'] + all_filings[i + 2]['financials']['income_statement']['revenues']['value'] + all_filings[i + 3]['financials']['income_statement']['revenues']['value']
                except KeyError:
                    quarterly_sales.append([symbol, end_date, year, "Q4", sales_label, math.nan])
                    continue

                quarterly_sales.append([symbol, end_date, year, "Q4", sales_label, sales - q3_ytd_sales])
            else:
                quarterly_sales.append([symbol, end_date, year, "Q4", sales_label, math.nan])
        else:
            quarterly_sales.append([symbol, end_date, year, period, sales_label, sales])

    if len(quarterly_sales) < 6:
        for i in range(0, 6 - len(quarterly_sales)):
            quarterly_sales.append([None, None, None, None, None, math.nan])

    # create pandas dataframes from the collected sales data
    quarterly_sales_df = pandas.DataFrame(quarterly_sales, columns = ['Ticker', 'End Date', 'Year', 'Period', 'Label', 'Sales'])
    annual_sales_df = pandas.DataFrame(annual_sales, columns = ['Ticker', 'End Date', 'Year', 'Period', 'Label', 'Sales'])

    # QUARTERLY SALES GROWTH CALCULATION

    # calculate sales growth for the two most recent quarters (compared to the same quarter the prior year)
    quarterly_sales_column = quarterly_sales_df['Sales']

    sales_one_year_change = percent_change(quarterly_sales_column[4], quarterly_sales_column[0])
    sales_previous_quarter_one_year_change = percent_change(quarterly_sales_column[5], quarterly_sales_column[1])

    # ANNUAL SALES GROWTH CALCULATION

    # calculate annual sales growth rate over the past 2-5 years
    annual_sales_column = annual_sales_df['Sales']
    annual_reports_count = len(annual_sales_column)

    if annual_reports_count < 2:
        annual_sales_growth_rate = math.nan
    else:
        annual_sales_change_total = 0
        for i in range(0, annual_reports_count - 1):
            annual_sales_change_total += percent_change(annual_sales_column[i + 1], annual_sales_column[i])

        annual_sales_growth_rate = annual_sales_change_total / (annual_reports_count - 1)

    # SALES STRENGTH CALCULATION

    # ideally, sales_strength = (sales_one_year_change + sales_previous_quarter_one_year_change + annual_sales_growth_rate) / 3

    # account for situations where not enough data is available
    sales_strength_criteria = [sales_one_year_change, sales_previous_quarter_one_year_change, annual_sales_growth_rate]

    available_criteria_count = 0
    criteria_sum = 0
    for criteria in sales_strength_criteria:
        if not math.isnan(criteria):
            available_criteria_count += 1
            criteria_sum += criteria

    if available_criteria_count > 0:
        sales_strength = criteria_sum / available_criteria_count
    else:
        sales_strength = math.nan

    # avoid stocks with less than 20% sales growth Q/Q
    if not math.isnan(sales_one_year_change) and sales_one_year_change < 20.0:
        sales_strength = math.nan

    print(f"{symbol} ({n} of {len(symbol_list)}) sales strength: {sales_strength} | {n / len(symbol_list) * 100:.0f}% percent complete")

    sales_strength_array.append(sales_strength)
    used_symbols.append(symbol)

    if show_extra_information:
        print(f"Sales Q/Q:\t{sales_one_year_change:.0f}%, {sales_previous_quarter_one_year_change:.0f}%")
        print(f"Sales Y/Y Growth Rate:\t{annual_sales_growth_rate:.0f}%")
        print("")
        print(f"Available Criteria Count:\t{available_criteria_count}")
        print(f"Criteria Sum:\t{criteria_sum:.2f}")
        print("")
        print(f"Sales Strength:\t{sales_strength:.2f}")
        print("")
        print(quarterly_sales_df)
        print("")
        print(annual_sales_df)

    if show_responses:
        print("")
        for filing in all_filings:
            print(filing)

sales_strength_data = pandas.DataFrame(sales_strength_array, columns=['Sales Strength'], index=used_symbols)

screen.generate(sales_strength_data, "Sales Strength.xlsx")
