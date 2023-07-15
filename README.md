# Growth-Stock-Screener

An automated stock screening system which isolates and ranks top-tier growth companies based on relative strength, price action, quarterly revenue, and liquidity.

### Screen Iterations

An initial list of stocks from which to screen is sourced from NASDAQ. Then, the following screen iterations are executed sequentially:

#### Iteration 1: Relative Strength

The market's strongest stocks are determined by calculating a raw weighted average percentage price change over the last 12 months of trading. A 40% weight is attributed to the most recent quarter, while the previous three quarters each receive a weight of 20%.

$$ RS (raw) = 0.2(Q_1 \%\delta) + 0.2(Q_2 \%\delta) + 0.2(Q_3 \%\delta) + 0.4(Q_4 \%\delta) $$

These raw values are then assigned a percentile rank from 0-100 and turned into RS ratings. By default, only stocks with a relative strength rating greater than or equal to 90 make it through this stage of screening.

#### Iteration 2: Liquidity

All micro-cap companies and penny stocks are filtered out based on the following criteria:

$$
\begin{aligned}
Market Cap &>= \$1B
Price &>= \$10
Volume 50 Day SMA &>= 100,000 shares
\end{aligned}
$$

#### Iteration 3: Trend

All stocks which are not in a stage-2 uptrend are filtered out.

A stage two uptrend is defined as follows:

$$
\begin{aligned}
Price >= 50 Day SMA
Price >= 200 Day SMA
10 Day SMA >= 21 Day EMA >= 50 Day SMA
Price within 50% of YTD High
\end{aligned}
$$

#### Iteration 4: Institutional Accumulation

Any stocks with a decrease in fund-ownership are excluded at this point. Changes in institutional holdings are sourced from NASDAQ.
