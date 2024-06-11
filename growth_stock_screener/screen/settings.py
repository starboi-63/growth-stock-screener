import multiprocessing

# ITERATIONS (modify these values as desired)

# Iteration 1: Relative Strength
min_rs: int = 90  # minimum RS rating to pass (integer from 0-100)

# Iteration 2: Liquidity
min_market_cap: float = 1000000000  # minimum market cap (USD)
min_price: float = 10               # minimum price (USD)
min_volume: int = 100000            # minimum 50-day average volume

# Iteration 3: Trend
trend_settings = {
    "Price >= 50-day SMA": True,               # set values to 'True' or 'False'
    "Price >= 200-day SMA": True,              # ^
    "10-day SMA >= 20-day SMA": True,          # ^ 
    "20-day SMA >= 50-day SMA": True,          # ^
    "Price within 50% of 52-week High": True,  # ^
}

# Iteration 4: Revenue Growth
min_growth_percent: float = 25  # minimum revenue growth for a quarter compared to the same quarter 1 year ago (percentage)
protected_rs: int = 97          # minimum RS rating to bypass revenue screen iteration (see README)

# Iteration 5: Institutional Accumulation
# (no parameters to modify)

# THREADS (manually set the following value if the screener reports errors during the "Trend" or "Institutional Accumulation" iterations)
# Recommended values are 1-10. Currently set to 3/4 the number of CPU cores on the system (with a max of 10)

# Thread Pool Size
threads: int = min(int(multiprocessing.cpu_count() * 0.75), 10)  # number of concurrent browser instances to fetch dynamic data (positive integer)
