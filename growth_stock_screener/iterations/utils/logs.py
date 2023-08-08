from termcolor import colored, cprint


def print_status(process: str, stage: int, starting: bool) -> None:
    """Print a header or footer for each screen iteration."""
    if starting:
        print(
            colored(f"\n****** Begin Stage {stage} [", "cyan"),
            colored(f"{process}", "white"),
            colored("] ******\n", "cyan"),
            sep="",
        )
    else:
        print(
            colored(f"\n****** Stage {stage} [", "cyan"),
            colored(f"{process}", "white"),
            colored("] Finished ******\n", "cyan"),
            sep="",
        )


def skip_message(symbol: str, message: str) -> str:
    """Return a custom message logging screening errors."""
    return colored(f"\nSkipping {symbol} ({message}) . . .\n", "red")


def filter_message(symbol: str) -> str:
    """Return a custom message for logging when a stock is filtered out by a screen."""
    return f"\n{symbol} filtered out.\n"


def message(message: str) -> str:
    """Return a custom message for logging purposes."""
    return f"\n{message}\n"
