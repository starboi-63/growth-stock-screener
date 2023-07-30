from utils.logging import *
from utils.outfiles import *
from utils.calculations import *

# constants
min_growth_percent = 25

# print header message to terminal
process_name = "Revenue Growth"
process_stage = 4
print_status(process_name, process_stage, True)
print(f"Minimum quarterly revenue growth to pass: {min_growth_percent}%")
