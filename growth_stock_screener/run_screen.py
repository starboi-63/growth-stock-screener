from iterations.utils import *
from datetime import datetime
from termcolor import cprint, colored

# print banner
banner = """
   ______                   __  __       _____ __             __      _____                                    
  / ____/________ _      __/ /_/ /_     / ___// /_____  _____/ /__   / ___/_____________  ___  ____  ___  _____
 / / __/ ___/ __ \ | /| / / __/ __ \    \__ \/ __/ __ \/ ___/ //_/   \__ \/ ___/ ___/ _ \/ _ \/ __ \/ _ \/ ___/
/ /_/ / /  / /_/ / |/ |/ / /_/ / / /   ___/ / /_/ /_/ / /__/ ,<     ___/ / /__/ /  /  __/  __/ / / /  __/ /    
\____/_/   \____/|__/|__/\__/_/ /_/   /____/\__/\____/\___/_/|_|   /____/\___/_/   \___/\___/_/ /_/\___/_/     
"""
cprint(banner, "red")

# run screen iterations
import iterations.nasdaq_listings

# import iterations.relative_strength
# import iterations.liquidity
# import iterations.trend
# import iterations.revenue_growth
# import iterations.institutional_accumulation


# # open screen results as a DataFrame
# final_iteration = "institutional_accumulation"
# df = open_outfile(final_iteration)

# # determine the current time
# time = datetime.now()
# time_string = time.strftime("%Y-%m-%d %H-%M-%S")

# # create a .csv outfile
# outfile_name = f"screen_results {time_string}.csv"
# df.to_csv(outfile_name)

# print(f"\nDONE! (created {outfile_name})")
