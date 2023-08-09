from iterations.utils import *
from datetime import datetime
from termcolor import cprint, colored

# print banner
print_banner()
time = datetime.now()
print(
    colored("\t\t\t\t\t Growth Stock Screener:", "cyan"),
    colored(time.strftime("%m/%d/%Y %H:%M:%S"), "cyan"),
)

# run screen iterations
import iterations.nasdaq_listings
import iterations.relative_strength

# import iterations.liquidity
# import iterations.trend
# import iterations.revenue_growth
# import iterations.institutional_accumulation


# # open screen results as a DataFrame
# final_iteration = "institutional_accumulation"
# df = open_outfile(final_iteration)


time_string = time.strftime("%Y-%m-%d %H-%M-%S")

# # create a .csv outfile
# outfile_name = f"screen_results {time_string}.csv"
# df.to_csv(outfile_name)

# print(f"\nDONE! (created {outfile_name})")
