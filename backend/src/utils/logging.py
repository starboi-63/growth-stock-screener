def print_status(process: str, stage: int, starting: bool) -> None:
    """Print a header or footer for each screen iteration."""
    if starting:
        print(f"\n****** Begin Stage {stage} [{process}] ******\n")
    else:
        print(f"\n****** Stage {stage} [{process}] Finished ******\n")


def skip_message(symbol: str, message: str) -> str:
    """Return a custom message logging screening errors."""
    return f"\nSkipping {symbol} ({message}) . . .\n"


def filter_message(symbol: str) -> str:
    """Return a custom message for logging when a stock is filtered out by a screen."""
    return f"\n{symbol} filtered out.\n"
