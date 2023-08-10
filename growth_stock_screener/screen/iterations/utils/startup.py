from termcolor import cprint, colored


def print_banner() -> None:
    """Print an ASCII art banner for the growth stock screener."""
    banner = [
        "\n",
        "\n                              o",
        "\n",
        "\n        .                                                              .",
        "\n                .",
        "\n .",
        "\n                                                                               o",
        "\n     dBBBBBb dBBBBb   dBBBBP dB'dB'dB'dBBBBBBP dB',BP",
        "\n                ,BP  dB',BP dB'dB'dB'         dB',BP  .",
        "\n   dB' dBB' dBBBBP  dB',BP dB'dB'dB'   dBp   dBBBBP",
        "\n  dB'  ,B' dBP BB  dB',BP dB'dB'dB'   dBP   dB',BP",
        "\n dBBBBBB' dBP  BB dBBBBP dBBBBBBP    dBP   dB'.BP",
        "\n",
        "\n                                             dBBBBBP dBBBB BBBBBb   dBBBP  dBBBP  dBBB  ,BP",
        "\n                                .                   dB'       ,BP                dB'BB ,BP",
        "\n                   .               |       dBBBBBP dB'    dBBBBP  dBBP   dBBP   dB' BB,BP",
        "\n                                 --o--        ,BP dB'    dBP BB  dBP    dBP    dB'  B,BP",
        "\n                                   |     dBBBBBP dBBBBP dBP  BB dBBBBP dBBBBP dB'   BBP",
        "\n",
        "\n                                                                                  .",
        "\n                      .",
        "\n              o              Targeting sequence initiated . . .",
        "\n                              Locking on to tickers [###-----]",
        "\n                                                                          .",
        "\n",
    ]

    cprint("".join(banner), attrs=["bold"])


print_banner()
