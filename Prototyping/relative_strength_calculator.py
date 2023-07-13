import pandas
import requests
import math
import scipy.stats
import time

# set to true if extra information is desired (ex. for debugging)
show_extra_information = False


# calculate percent change between two values
def percent_change(initial, final):
    return ((final - initial) / initial) * 100


# get closing price of candle from json API response
def get_close(response_, index):
    return response_[index]['close'] if 0 <= index < len(response_) else math.nan


# get date of candle from json API response
def get_date(response_, index):
    return pandas.to_datetime(response_[index]['datetime'], unit='ms') if 0 <= index < len(response_) else math.nan


# attempt to retrieve stock data from the API; stop retrying after a certain number of attempts
def request(url_, parameters_, max_attempts, data_location):
    response = None

    tries = 0
    while tries < max_attempts:
        # perform the get request and store data in json format
        tries += 1

        try:
            response = requests.get(url_, parameters_).json()[data_location]
        except:
            # stop retrying if there is no response after the max number of attempts
            if tries == max_attempts:
                break

            print("Retrying . . .")

            # waiting 30 seconds and then trying again generally fixes most errors
            time.sleep(30)
            continue

        break

    return response


# generate a list of ticker symbols to use for relative strength calculations from an excel file
stock_list = pandas.read_excel('pre-screens/All Non-Penny Stocks.xlsx')['Symbol']
etf_list = pandas.read_excel('pre-screens/Sector ETFs.xlsx')['Symbol']

symbol_list = etf_list.append(stock_list)

# parameters for the API get requests
parameters_historical = \
    {
        'apikey': 'HN1E46JV9UHWTKBAJJIV0XLKELAQJ9RS',
        'periodType': 'year',
        'period': 1,
        'frequencyType': 'daily',
        'frequency': 1
    }

# a list of ticker symbols which successfully returned data
used_symbols = []
# an array in which collected stock data will be placed
stock_data_array = []

# attempt to collect data from each ticker symbol
i = 1
for symbol in symbol_list:
    # ACQUIRE STOCK DATA WITH GET REQUESTS AND PRINT HEADER

    # the url for the API get requests
    url_historical = "https://api.tdameritrade.com/v1/marketdata/{}/pricehistory".format(symbol)

    # skip the ticker symbol if it isn't alphabetic
    if not str.isalpha(str(symbol)):
        print(f"Skipping {symbol} (ticker symbol contains non-alphabetic characters)")
        i += 1
        continue

    # retrieve data from the API
    response_historical = request(url_historical, parameters_historical, 4, 'candles')

    # skip the ticker symbol if no response was obtained
    if response_historical is None:
        print(f"Skipping {symbol} (failed to retrieve data)")
        i += 1
        continue

    # the number of candles contained in the historical response
    length = len(response_historical)

    # CALCULATE RAW RELATIVE STRENGTH

    # obtain prices at the start and end of each trailing quarter for calculating relative strength, if possible
    start_price = get_close(response_historical, 0)
    # On average, there are 253 trading days in a year. Since 253 has a remainder of 1 when divided by 4, the most
    # recent quarter is given that "extra" day for simplicity's sake. If you prefer, you can change the
    # values to only use 252 days in your calculation.
    q1_start_price = get_close(response_historical, length - 253)
    q1_end_price = get_close(response_historical, length - 189)
    q2_start_price = get_close(response_historical, length - 190)
    q2_end_price = get_close(response_historical, length - 126)
    q3_start_price = get_close(response_historical, length - 127)
    q3_end_price = get_close(response_historical, length - 63)
    q4_start_price = get_close(response_historical, length - 64)
    current_price = get_close(response_historical, length - 1)

    # calculate the price percent change over the past four quarters (on a TTM basis)
    q1_percent_change = percent_change(q1_start_price, q1_end_price)
    q2_percent_change = percent_change(q2_start_price, q2_end_price)
    q3_percent_change = percent_change(q3_start_price, q3_end_price)
    q4_percent_change = percent_change(q4_start_price, current_price)
    # for stocks that haven't traded one full quarter, take the percent change between the ipo price and the current price
    ipo_percent_change = percent_change(start_price, current_price)

    # the most recent quarterly percent change is given a 40% weight while the three others are given a 20% weight
    relative_strength = (0.4 * q4_percent_change) + (0.2 * (q3_percent_change + q2_percent_change + q1_percent_change))

    # account for cases where a stock has not traded for a full year yet
    if math.isnan(q1_percent_change):
        relative_strength = (0.6 * q4_percent_change) + (0.2 * (q3_percent_change + q2_percent_change))

    if math.isnan(q2_percent_change):
        relative_strength = (0.8 * q4_percent_change) + (0.2 * q3_percent_change)

    if math.isnan(q3_percent_change):
        relative_strength = q4_percent_change

    if math.isnan(q4_percent_change):
        relative_strength = ipo_percent_change

    # skip the ticker symbol if fewer than 5 trading days worth of data is available
    if math.isnan(get_close(response_historical, length - 6)):
        print(f"Skipping {symbol} (fewer than 5 trading days of data available)")
        i += 1
        continue

    # print header
    print(f"{symbol} ({i} of {len(symbol_list)}) relative strength: {relative_strength:.3f} | {i / len(symbol_list) * 100:.0f}% Percent Complete")

    # print data below the header
    if show_extra_information:
        print("Response Length: {}d | RS Raw: {:.2f}".format(length, relative_strength))
        print("Q1: ${:.2f} | Q2: ${:.2f} | Q3: ${:.2f} | Q4: ${:.2f} | Start Price: ${:.2f} | Current: ${:.2f}".format(q1_start_price, q2_start_price, q3_start_price, q4_start_price, start_price, current_price))
        print("Q1: {:.2f}% | Q2: {:.2f}% | Q3: {:.2f}% | Q4: {:.2f}% | Start-End: {:.2f}%".format(q1_percent_change, q2_percent_change, q3_percent_change, q4_percent_change, ipo_percent_change))
        print("\n")

    # ADD DATA TO ONE CENTRAL ARRAY FOR CONVERSION TO PANDAS DATAFRAME

    stock_data_array.append([current_price, relative_strength])
    used_symbols.append(symbol)
    i += 1

# create a pandas dataframe with the proper column and index labels
stock_data = pandas.DataFrame(stock_data_array, columns=['Close', 'Raw RS'], index=used_symbols)

# DETERMINE IBD STYLE PERCENTILE RELATIVE STRENGTH FOR EACH STOCK

# a list which will contain relative strength values (not to be confused with the raw relative strength values)
relative_strength_rating_list = []

# based on the entire set of raw relative strength values, assign a percentile relative strength to each stock
for rs in stock_data['Raw RS']:
    relative_strength_rating = int(scipy.stats.percentileofscore(stock_data['Raw RS'], rs))
    # following Investors Business Daily's style, the highest and lowest possible relative strengths are 99 and 1 respectively
    relative_strength_rating = 99 if relative_strength_rating == 100 else relative_strength_rating
    relative_strength_rating = 1 if relative_strength_rating == 0 else relative_strength_rating
    relative_strength_rating_list.append(relative_strength_rating)

# insert the list of percentile relative strengths into the pandas dataframe
stock_data.insert(1, 'Relative Strength', relative_strength_rating_list)

print("\n{}".format(stock_data))

# generate a .csv file from the pandas dataframe
file_name_csv = "relative_strength_data.csv"
stock_data.to_csv("pre-screens/python intermediates/" + file_name_csv)

# add the word "Symbol" to the previously generated .csv file and save it as a new .csv file
with open("pre-screens/python intermediates/" + file_name_csv, "r") as data:
    modified_csv = "Symbol" + data.read()

file_name_modified_csv = "modified_relative_strength_data.csv"
modified_rs_data = open("pre-screens/python intermediates/" + file_name_modified_csv, "w")
modified_rs_data.write(modified_csv)

# generate a .xlsx file from the modified .csv file
file_name_excel = "Relative Strength.xlsx"
stock_data = pandas.read_csv("pre-screens/python intermediates/" + file_name_modified_csv)
stock_data.to_excel("results/" + file_name_excel)

print(f"Generated \"{file_name_excel}\"")
