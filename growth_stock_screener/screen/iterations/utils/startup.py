from termcolor import cprint, colored
from datetime import datetime
from ...settings import *


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


def print_settings(time: datetime) -> None:
    """Print a heading displaying screen settings."""
    main_color = "blue"
    setting_name_color = "dark_grey"
    setting_value_color = "light_grey"
    color_len = 9
    bold_len = 4

    main_time = " ".join(
        [
            colored("Growth Stock Screener:", main_color, attrs=["bold"]),
            colored(time.strftime("%m/%d/%Y %H:%M:%S"), "white"),
        ]
    )
    main_time_len = len(main_time) - (2 * color_len) - bold_len

    rs = " ".join(
        [
            colored("Minimum RS Rating:", setting_name_color),
            colored(min_rs, setting_value_color),
            "|",
            colored("Minimum RS Rating to Bypass Revenue Screen:", setting_name_color),
            colored(protected_rs, setting_value_color),
        ]
    )
    rs_len = len(rs) - (4 * color_len)

    liquidity_1 = " ".join(
        [
            colored("Minimum Market Cap:", setting_name_color),
            colored(f"${min_market_cap:,.0f}", setting_value_color),
            "|",
            colored("Minimum Price:", setting_name_color),
            colored(f"${min_price:,.2f}", setting_value_color),
        ]
    )
    liquidity_1_len = len(liquidity_1) - (4 * color_len)

    liquidity_2 = " ".join(
        [
            colored("Minimum 50-day Average Volume:", setting_name_color),
            colored(f"{min_volume:,.0f} shares", setting_value_color),
        ]
    )
    liquidity_2_len = len(liquidity_2) - (2 * color_len)

    trend_1 = " ".join(
        [
            colored("Price >= 50-day SMA:", setting_name_color),
            status(trend_settings["Price >= 50-day SMA"]),
            "|",
            colored("Price >= 200-day SMA:", setting_name_color),
            status(trend_settings["Price >= 200-day SMA"]),
        ]
    )
    trend_1_len = len(trend_1) - (4 * color_len)

    trend_2 = " ".join(
        [
            colored("10-day SMA >= 20-day SMA:", setting_name_color),
            status(trend_settings["10-day SMA >= 20-day SMA"]),
            "|",
            colored("20-day SMA >= 50-day SMA:", setting_name_color),
            status(trend_settings["20-day SMA >= 50-day SMA"]),
        ]
    )
    trend_2_len = len(trend_2) - (4 * color_len)

    trend_3 = " ".join(
        [
            colored("Price Within 50% of 52-week High:", setting_name_color),
            status(trend_settings["Price within 50% of 52-week High"]),
        ]
    )
    trend_3_len = len(trend_3) - (2 * color_len)

    revenue = " ".join(
        [
            colored("Minimum Quarterly Revenue Growth:", setting_name_color),
            colored(f"{min_growth_percent}%", setting_value_color),
        ]
    )
    revenue_len = len(revenue) - (2 * color_len)

    lengths = [
        main_time_len,
        rs_len,
        liquidity_1_len,
        liquidity_2_len,
        trend_1_len,
        trend_2_len,
        trend_3_len,
    ]
    max_len = max(lengths)

    print(
        "           Change screen settings in growth_stock_screener/screen/settings.py"
    )
    print()
    print("         [", append_spaces(main_time, max_len - main_time_len), "]")
    print("+ -- --=>[", append_spaces(rs, max_len - rs_len), "]")
    print("+ -- --=>[", append_spaces(liquidity_1, max_len - liquidity_1_len), "]")
    print("+ -- --=>[", append_spaces(liquidity_2, max_len - liquidity_2_len), "]")
    print("+ -- --=>[", append_spaces(trend_1, max_len - trend_1_len), "]")
    print("+ -- --=>[", append_spaces(trend_2, max_len - trend_2_len), "]")
    print("+ -- --=>[", append_spaces(trend_3, max_len - trend_3_len), "]")
    print("+ -- --=>[", append_spaces(revenue, max_len - revenue_len), "]")
    print()


def status(is_enabled: bool) -> str:
    """Return a colored string denoting whether a setting is enabled or disabled."""
    return colored("Enabled", "green") if is_enabled else colored("Disabled", "red")


def append_spaces(input: str, n: int) -> str:
    """Append whitespace to the end of a string."""
    return "".join([input, "".join([" " for i in range(n)])])
