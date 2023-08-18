from screen.iterations.utils import *
from datetime import datetime
import time
from termcolor import cprint, colored

# constants
current_time = datetime.now()

# print banner and heading
print_banner()
print_settings(current_time)

# check Python version
min_python_version = "3.11"
assert_python_updated(min_python_version)

# wait for user to press enter
input("Press Enter to run screen . . .")

# track start time
start = time.perf_counter()

# run screen iterations
import screen.iterations.nasdaq_listings

# import screen.iterations.relative_strength
# import screen.iterations.liquidity
# import screen.iterations.trend
# import screen.iterations.revenue_growth
# import screen.iterations.institutional_accumulation

# open screen results as a DataFrame
final_iteration = "institutional_accumulation"
df = open_outfile(final_iteration)

# create a .csv outfile
time_string = current_time.strftime("%Y-%m-%d %H-%M-%S")
outfile_name = f"screen_results {time_string}.csv"
df.to_csv(outfile_name)

# track end time
end = time.perf_counter()

# notify user when finished
print_done_message(end - start, outfile_name)
