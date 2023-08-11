from termcolor import cprint, colored
from datetime import datetime

# from ...settings import *

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
    "Price >= 200-day SMA": False,
    "10-day SMA >= 20-day SMA": False,
    "20-day SMA >= 50-day SMA": True,
    "Price within 50% of 52-week High": True,
}

# Iteration 4: Revenue Growth
min_growth_percent = 25
protected_rs = 97

# Iteration 5: Institutional Accumulation
# (no parameters to modify)


def print_banner() -> None:
    """Print an ASCII art banner for the growth stock screener."""
    banner = [
        "\n",
        colored(
            "\n                              o",
            "white",
            attrs=["bold"],
        ),
        "\n",
        colored(
            "\n        .                                                              .",
            "white",
            attrs=["bold"],
        ),
        colored(
            "\n                .",
            "white",
            attrs=["bold"],
        ),
        colored(
            "\n .",
            "white",
            attrs=["bold"],
        ),
        colored(
            "\n                                                                               o",
            "white",
            attrs=["bold"],
        ),
        colored(
            "\n     dBBBBBb dBBBBb   dBBBBP dB'dB'dB'dBBBBBBP dB',BP",
            "blue",
            attrs=["bold"],
        ),
        colored(
            "\n                ,BP  dB',BP dB'dB'dB'         dB',BP  ",
            "blue",
            attrs=["bold"],
        ),
        colored(
            ".",
            "white",
            attrs=["bold"],
        ),
        colored(
            "\n   dB' dBB' dBBBBP  dB',BP dB'dB'dB'   dBp   dBBBBP",
            "blue",
            attrs=["bold"],
        ),
        colored(
            "\n  dB'  ,B' dBP BB  dB',BP dB'dB'dB'   dBP   dB',BP",
            "blue",
            attrs=["bold"],
        ),
        colored(
            "\n dBBBBBB' dBP  BB dBBBBP dBBBBBBP    dBP   dB'.BP",
            "blue",
            attrs=["bold"],
        ),
        "\n",
        colored(
            "\n                                             dBBBBBP",
            "red",
            attrs=["bold"],
        ),
        colored(
            " dBBBB BBBBBb   dBBBP  dBBBP  dBBB  ,BP",
            "blue",
            attrs=["bold"],
        ),
        colored(
            "\n                                .",
            "white",
            attrs=["bold"],
        ),
        colored(
            "                   dB'       ,BP                dB'BB ,BP",
            "blue",
            attrs=["bold"],
        ),
        colored(
            "\n                   .",
            "white",
            attrs=["bold"],
        ),
        colored(
            "               |",
            "light_grey",
            attrs=["bold"],
        ),
        colored(
            "       dBBBBBP",
            "red",
            attrs=["bold"],
        ),
        colored(
            " dB'    dBBBBP  dBBP   dBBP   dB' BB,BP",
            "blue",
            attrs=["bold"],
        ),
        colored(
            "\n                                 --o--",
            "light_grey",
            attrs=["bold"],
        ),
        colored(
            "        ,BP",
            "red",
            attrs=["bold"],
        ),
        colored(
            " dB'    dBP BB  dBP    dBP    dB'  B,BP",
            "blue",
            attrs=["bold"],
        ),
        colored(
            "\n                                   |",
            "light_grey",
            attrs=["bold"],
        ),
        colored(
            "     dBBBBBP",
            "red",
            attrs=["bold"],
        ),
        colored(
            " dBBBBP dBP  BB dBBBBP dBBBBP dB'   BBP",
            "blue",
            attrs=["bold"],
        ),
        "\n",
        colored(
            "\n                                                                                  .",
            "white",
            attrs=["bold"],
        ),
        colored(
            "\n                      .",
            "white",
            attrs=["bold"],
        ),
        colored(
            "\n              o",
            "white",
            attrs=["bold"],
        ),
        colored(
            "              Targeting sequence initiated . . .",
            "dark_grey",
        ),
        colored(
            "\n                              Locking on to tickers [###-----]",
            "dark_grey",
        ),
        colored(
            "\n                                                                          .",
            "white",
            attrs=["bold"],
        ),
        "\n",
    ]

    print("".join(banner))


def print_heading() -> None:
    """Print a heading displaying screen settings."""
    main_color = "blue"
    setting_name_color = "dark_grey"
    setting_value_color = "white"
    color_length = 9
    bold_length = 4

    main_time = " ".join(
        [
            colored("Growth Stock Screener:", main_color, attrs=["bold"]),
            colored("time goes here", "white")
            # colored(time.strftime("%m/%d/%Y %H:%M:%S"), "white"),
        ]
    )
    main_time_length = len(main_time) - (2 * color_length) - bold_length

    rs = " ".join(
        [
            colored("Minimum RS rating:", setting_name_color),
            colored(min_rs, setting_value_color),
        ]
    )
    rs_length = len(rs) - (2 * color_length)

    liquidity_1 = " ".join(
        [
            colored("Minimum Market Cap:", setting_name_color),
            colored(f"${min_market_cap:,.0f}", setting_value_color),
            "|",
            colored("Minimum Price:", setting_name_color),
            colored(f"${min_price:,.2f}", setting_value_color),
        ]
    )
    liquidity_1_length = len(liquidity_1) - (4 * color_length)

    liquidity_2 = " ".join(
        [
            colored("Minimum 50-day Average Volume:", setting_name_color),
            colored(f"{min_volume:,.0f} shares", setting_value_color),
        ]
    )
    liquidity_2_length = len(liquidity_2) - (2 * color_length)

    trend_1 = " ".join(
        [
            colored("Price >= 50-day SMA:", setting_name_color),
            status(trend_settings["Price >= 50-day SMA"]),
            "|",
            colored("Price >= 200-day SMA:", setting_name_color),
            status(trend_settings["Price >= 200-day SMA"]),
        ]
    )
    trend_1_length = len(trend_1) - (4 * color_length)

    trend_2 = " ".join(
        [
            colored("10-day SMA >= 20-day SMA:", setting_name_color),
            status(trend_settings["10-day SMA >= 20-day SMA"]),
            "|",
            colored("20-day SMA >= 50-day SMA:", setting_name_color),
            status(trend_settings["20-day SMA >= 50-day SMA"]),
        ]
    )
    trend_2_length = len(trend_2) - (4 * color_length)

    trend_3 = " ".join(
        [
            colored("Price Within 50% of 52-week High:", setting_name_color),
            status(trend_settings["Price within 50% of 52-week High"]),
        ]
    )
    trend_3_length = len(trend_3) - (2 * color_length)

    lengths = [
        main_time_length,
        rs_length,
        liquidity_1_length,
        liquidity_2_length,
        trend_1_length,
        trend_2_length,
        trend_3_length,
    ]
    longest_length = max(lengths)

    print("=[", append_spaces(main_time, (longest_length - main_time_length)), "]")


def status(is_enabled: bool) -> str:
    """Return a colored string denoting whether a setting is enabled or disabled."""
    return colored("Enabled", "green") if is_enabled else colored("Disabled", "red")


def append_spaces(input: str, n: int) -> str:
    """Append whitespace to the end of a string."""
    return "".join([input, "".join([" " for i in range(n)])])


print_banner()
print_heading()
