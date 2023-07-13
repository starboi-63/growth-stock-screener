import pandas


def screen(input_filepath, rs_data):
    symbol_list = pandas.read_excel(input_filepath)['Symbol']

    # array to contain located data
    located_data = []

    # search the relative strength data for ticker symbols in the growth stock list
    for symbol in symbol_list:
        line_data = []

        try:
            for item in rs_data.loc[rs_data['Symbol'] == symbol].iloc[0]:
                line_data.append(item)
        except:
            print(symbol + " not found")

        located_data.append(line_data)

    screened_stock_data = pandas.DataFrame(located_data, columns = ['Symbol', 'Close', 'Relative Strength', 'Raw RS'])

    return screened_stock_data


def generate(screened_stock_data, output_filename):
    # generate an excel file containing the results
    screened_stock_data.to_excel("results/" + output_filename)
    print(f"\nGenerated \"{output_filename}\"")
