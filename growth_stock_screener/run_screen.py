from screen.iterations.utils import *
from datetime import datetime
from termcolor import cprint, colored

# print banner
print_banner()
time = datetime.now()
print_heading(time)

# wait for user to press enter
input("Press Enter to run screen . . .")

# run screen iterations
import screen.iterations.nasdaq_listings
import screen.iterations.relative_strength
import screen.iterations.liquidity
import screen.iterations.trend
import screen.iterations.revenue_growth
import screen.iterations.institutional_accumulation

# open screen results as a DataFrame
final_iteration = "institutional_accumulation"
df = open_outfile(final_iteration)

# create a .csv outfile
time_string = time.strftime("%Y-%m-%d %H-%M-%S")
outfile_name = f"screen_results {time_string}.csv"
df.to_csv(outfile_name)

cprint(f"\nDONE! (created {outfile_name})", "green", attrs=["bold"])
