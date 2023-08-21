import multiprocessing

# modify these values as desired

# Iteration 1: Relative Strength
min_rs = 90  # minimum RS rating to pass (must be an integer from 0-100)

# Iteration 2: Liquidity
min_market_cap = 1000000000  # minimum market cap to pass in USD
min_price = 10  # minimum price to pass in USD
min_volume = 100000  # minimum 50-day average volume to pass in shares

# Iteration 3: Trend
# set values to 'True' or 'False' to enable or disable checks
trend_settings = {
    "Price >= 50-day SMA": True,
    "Price >= 200-day SMA": True,
    "10-day SMA >= 20-day SMA": True,
    "20-day SMA >= 50-day SMA": True,
    "Price within 50% of 52-week High": True,
}

# Iteration 4: Revenue Growth
min_growth_percent = 25  # minimum revenue growth percent for a quarter compared to the same quarter 1 year ago
protected_rs = 97  # minimum RS rating to bypass revenue screen iteration (see README)

# Iteration 5: Institutional Accumulation
# (no parameters to modify)

# Thread Pool Size (the number of concurrent browser instances to fetch dynamic data)
threads = multiprocessing.cpu_count() // 1.25 # must be a positive integer (currently set to 3/4 the number of CPU cores on the system)
