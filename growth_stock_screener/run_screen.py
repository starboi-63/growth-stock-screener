from iterations.utils import *
from datetime import datetime
from termcolor import cprint, colored

# print banner
banner = """
   ______                   __  __       _____ __             __   
  / ____/________ _      __/ /_/ /_     / ___// /_____  _____/ /__ 
 / / __/ ___/ __ \ | /| / / __/ __ \    \__ \/ __/ __ \/ ___/ //_/ 
/ /_/ / /  / /_/ / |/ |/ / /_/ / / /   ___/ / /_/ /_/ / /__/ ,<    
\____/_/   \____/|__/|__/\__/_/ /_/   /____/\__/\____/\___/_/|_|   
    _________                                                
   /   _____/ ___________   ____   ____   ____   ___________ 
   \_____  \_/ ___\_  __ \_/ __ \_/ __ \ /    \_/ __ \_  __ \\
   /\___/   \  \___|  | \/\  ___/\  ___/|   |  \  ___/|  | \/
  /_______  /\___  >__|    \___  >\___  >___|  /\___  >__|   
          \/     \/            \/     \/     \/     \/       
"""
cprint(banner, "cyan")

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

# # determine the current time
# time = datetime.now()
# time_string = time.strftime("%Y-%m-%d %H-%M-%S")

# # create a .csv outfile
# outfile_name = f"screen_results {time_string}.csv"
# df.to_csv(outfile_name)

# print(f"\nDONE! (created {outfile_name})")
