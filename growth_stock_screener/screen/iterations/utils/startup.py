from termcolor import cprint, colored


def print_banner() -> None:
    """Print an ASCII art banner for the growth stock screener."""
    banner = [
        "\n",
        colored("\n                              o", "white"),
        "\n",
        colored(
            "\n        .                                                              .",
            "white",
        ),
        colored("\n                .", "white"),
        colored("\n .", "white"),
        colored(
            "\n                                                                               o",
            "white",
        ),
        colored("\n     dBBBBBb dBBBBb   dBBBBP dB'dB'dB'dBBBBBBP dB',BP", "blue"),
        colored("\n                ,BP  dB',BP dB'dB'dB'         dB',BP  ", "blue"),
        colored(".", "white"),
        colored("\n   dB' dBB' dBBBBP  dB',BP dB'dB'dB'   dBp   dBBBBP", "blue"),
        colored("\n  dB'  ,B' dBP BB  dB',BP dB'dB'dB'   dBP   dB',BP", "blue"),
        colored("\n dBBBBBB' dBP  BB dBBBBP dBBBBBBP    dBP   dB'.BP", "blue"),
        "\n",
        colored("\n                                             dBBBBBP", "red"),
        colored(" dBBBB BBBBBb   dBBBP  dBBBP  dBBB  ,BP", "blue"),
        colored("\n                                .", "white"),
        colored("                   dB'       ,BP                dB'BB ,BP", "blue"),
        colored("\n                   .", "white"),
        colored("               |", "light_grey"),
        colored("       dBBBBBP", "red"),
        colored(" dB'    dBBBBP  dBBP   dBBP   dB' BB,BP", "blue"),
        colored("\n                                 --o--", "light_grey"),
        colored("        ,BP", "red"),
        colored(" dB'    dBP BB  dBP    dBP    dB'  B,BP", "blue"),
        colored("\n                                   |", "light_grey"),
        colored("     dBBBBBP", "red"),
        colored(" dBBBBP dBP  BB dBBBBP dBBBBP dB'   BBP", "blue"),
        "\n",
        colored(
            "\n                                                                                  .",
            "white",
        ),
        colored("\n                      .", "white"),
        colored("\n              o", "white"),
        colored("              Targeting sequence initiated . . .", "dark_grey"),
        colored(
            "\n                              Locking on to tickers [###-----]",
            "dark_grey",
        ),
        colored(
            "\n                                                                          .",
            "white",
        ),
        "\n",
    ]

    cprint("".join(banner), attrs=["bold"])


print_banner()
