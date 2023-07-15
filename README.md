# Growth-Stock-Screener

An automated stock screening system which isolates and ranks top-tier growth companies based on relative strength, price action, quarterly revenue, liquidity, and institutional demand.

### Screen Iterations

An initial list of stocks from which to screen is sourced from NASDAQ. Then, the following screen iterations are executed sequentially:

#### Iteration 1: Relative Strength

The market's strongest stocks are determined by calculating a raw weighted average percentage price change over the last 12 months of trading. A 40% weight is attributed to the most recent quarter, while the previous three quarters each receive a weight of 20%.

$$\text{RS (raw)} = 0.2(Q_1\ \percent\Delta) + 0.2(Q_2\ \%\Delta) + 0.2(Q_3\ \%\Delta) + 0.4(Q_4\ \%\Delta)$$

These raw values are then assigned a percentile rank from 0-100 and turned into RS ratings. By default, only stocks with a relative strength rating greater than or equal to 90 make it through this stage of screening.

#### Iteration 2: Liquidity

All micro-cap companies and penny stocks are filtered out based on the following criteria:

$$
\begin{aligned}
\text{Market Cap} &>= \$1\ \text{billion}\\
\text{Price} &>= \$10\\
\text{Volume}\ 50\ \text{day SMA} &>= 100,000\ \text{shares}
\end{aligned}
$$

#### Iteration 3: Trend

All stocks which are not in a stage-2 uptrend are filtered out.

A stage two uptrend is defined as follows:

$$
\begin{aligned}
\text{Price} &>= 50\ \text{day SMA}\\
\text{Price} &>= 200\ \text{day SMA}\\
10\ \text{day SMA} &>= 21\ \text{day EMA} >= 50\ \text{day SMA}\\
\text{Price} >= 50\%\ text{of YTD High}
\end{aligned}
$$

#### Iteration 4: Institutional Accumulation

Any stocks with a decrease in fund-ownership are excluded at this point. Changes in institutional holdings are sourced from NASDAQ.
