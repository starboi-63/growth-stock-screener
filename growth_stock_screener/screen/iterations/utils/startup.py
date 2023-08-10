from termcolor import cprint, colored


def print_banner() -> None:
    """Print an ASCII art banner for the growth stock screener."""
    banner = []
    banner.append("\n")
    banner.append("\n                              o")
    banner.append("\n")
    banner.append(
        "\n        .                                                              ."
    )
    banner.append("\n                .")
    banner.append("\n .")
    banner.append(
        "\n                                                                               o"
    )
    banner.append("\n     dBBBBBb dBBBBb   dBBBBP dB'dB'dB'dBBBBBBP dB',BP")
    banner.append("\n                ,BP  dB',BP dB'dB'dB'         dB',BP  .")
    banner.append("\n   dB' dBB' dBBBBP  dB',BP dB'dB'dB'   dBp   dBBBBP")
    banner.append("\n  dB'  ,B' dBP BB  dB',BP dB'dB'dB'   dBP   dB',BP")
    banner.append("\n dBBBBBB' dBP  BB dBBBBP dBBBBBBP    dBP   dB'.BP")
    banner.append("\n")
    banner.append(
        "\n                                             dBBBBBP dBBBB BBBBBb   dBBBP  dBBBP  dBBB  ,BP"
    )
    banner.append(
        "\n                                .                   dB'       ,BP                dB'BB ,BP"
    )
    banner.append(
        "\n                   .               |       dBBBBBP dB'    dBBBBP  dBBP   dBBP   dB' BB,BP"
    )
    banner.append(
        "\n                                 --o--        ,BP dB'    dBP BB  dBP    dBP    dB'  B,BP"
    )
    banner.append(
        "\n                                   |     dBBBBBP dBBBBP dBP  BB dBBBBP dBBBBP dB'   BBP"
    )
    banner.append("\n")
    banner.append(
        "\n                                                                                  ."
    )
    banner.append("\n                      .")
    banner.append("\n              o              Targeting sequence initiated . . .")
    banner.append("\n                              Locking on to tickers [###-----]")
    banner.append(
        "\n                                                                          ."
    )
    banner.append("\n")

    cprint("".join(banner), attrs=["bold"])


print_banner()
