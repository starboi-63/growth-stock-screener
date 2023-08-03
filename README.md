# Growth-Stock-Screener

An automated stock screening system which isolates and ranks top-tier growth companies based on relative strength, liquidity, trend, revenue growth, and institutional demand.

## Prerequisites

1. Internet Access
2. Firefox Installation

## Screen Iterations

An initial list of stocks from which to screen is sourced from _NASDAQ_. Then, the following screen iterations are executed sequentially:

### Iteration 1: Relative Strength

The market's strongest stocks are determined by calculating a raw weighted average percentage price change over the last $12$ months of trading. A $40\\%$ weight is attributed to the most recent quarter, while the previous three quarters each receive a weight of $20\\%$.

$$\text{RS (raw)} = 0.2(Q_1\ \\%\Delta) + 0.2(Q_2\ \\%\Delta) + 0.2(Q_3\ \\%\Delta) + 0.4(Q_4\ \\%\Delta)$$

These raw values are then assigned a _percentile rank_ from $0\to 100$ and turned into _RS ratings_. By default, only stocks with a relative strength rating greater than or equal to $90$ make it through this stage of screening.

### Iteration 2: Liquidity

All _micro-cap_ companies and _thinly traded_ stocks are filtered out based on the following criteria:

$$
\begin{aligned}
\text{Market Cap} &>= \$1\ \text{Billion}\\
\text{Price} &>= \$10\\
50\ \text{day Average Volume} &>= 100,000\ \text{Shares}
\end{aligned}
$$

### Iteration 3: Trend

All stocks which are not in a _stage-two_ uptrend are filtered out. A stage-two uptrend is defined as follows:

$$
\begin{aligned}
\text{Price} &>= 50\ \text{Day SMA}\\
\text{Price} &>= 200\ \text{Day SMA}\\
10\ \text{Day SMA} &>= 20\ \text{Day SMA} >= 50\ \text{Day SMA}\\
\text{Price} &>= 50\\%\ \text{of}\ 52\ \text{Week High}
\end{aligned}
$$

### Iteration 4: Revenue Growth

Only the most rapidly growing stocks with _high sales growth_ are allowed to pass this iteration of the screen. Specifically,
the percent increase in the most recent reported quarterly revenue versus a year ago must be at least $25\\%$; if available, the percent increase in the prior period versus the same quarter a year ago must also be at least $25\\%$.

The current market often factors in _future_ revenue growth; historically, this means certain exceptional stocks have exhibited super-performance _without_ having strong on-paper revenue growth (examples include NVDA, UPST, PLTR, etc.). To ensure that these stocks aren't needlessly filtered out, a small exception to revenue criteria is added: stocks with an $\text{RS} \geq 99$ can bypass revenue criteria and make it through this screen iteration.

### Iteration 5: Institutional Accumulation

Any stocks with a _net-decrease_ in institutional-ownership are excluded at this point. Institutional-ownership is measured by the total inflows and outflows in the most recent financial quarter. If institutional inflows exceed outflows, a stock will pass this iteration of the screen as it is under accumulation.
