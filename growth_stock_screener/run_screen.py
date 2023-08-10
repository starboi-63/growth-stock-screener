from screen.iterations.utils import *
from datetime import datetime
from termcolor import cprint, colored

# print banner
print_banner()
time = datetime.now()
print_heading(time)

# run screen iterations
import screen.iterations.nasdaq_listings
import screen.iterations.relative_strength
import screen.iterations.liquidity

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
