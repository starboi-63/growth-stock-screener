# modify these values as desired

# Iteration 1: Relative Strength
min_rs = 90  # minimum RS rating to pass (must be an integer from 0-100)

# Iteration 2: Liquidity
min_market_cap = 1000000000  # minimum market cap to pass in USD
min_price = 10  # minimum price to pass in USD
min_volume = 100000  # minimum 50-day average volume to pass in shares

# Iteration 3: Trend
trend_settings = {
    "Price >= 50-day SMA": True,
    "Price >= 200-day SMA": True,
    "10-day SMA >= 20-day SMA": True,
    "20-day SMA >= 50-day SMA": True,
    "Price within 50% of 52-week High": True,
}

# Iteration 4: Revenue Growth
min_growth_percent = 25
protected_rs = 97

# Iteration 5: Institutional Accumulation
# (no parameters to modify)
