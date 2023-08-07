# run screen iterations
# import iterations.nasdaq_listings
# import iterations.relative_strength
# import iterations.liquidity
import iterations.trend
import iterations.revenue_growth
import iterations.institutional_accumulation
from iterations.utils import *
from datetime import datetime

# open screen results as a DataFrame
final_iteration = "institutional_accumulation"
df = open_outfile(final_iteration)

# determine the current time
time = datetime.now()
time_string = time.strftime("%Y-%m-%d %H-%M-%S")

# create a .csv outfile
outfile_name = f"screen_results {time_string}"
df.to_csv(outfile_name)

print(f"\nDONE! (created {outfile_name}.csv)")
