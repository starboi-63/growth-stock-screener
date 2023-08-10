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


def print_heading(time: datetime) -> None:
    print(
        colored("\t\t\t Growth Stock Screener:", "blue"),
        colored(time.strftime("%m/%d/%Y %H:%M:%S"), "white"),
    )
