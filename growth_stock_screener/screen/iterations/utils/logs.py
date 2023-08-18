from termcolor import colored, cprint
from typing import Dict


def print_status(
    process: str, stage: int, starting: bool, elapsed_time: float = None
) -> None:
    """Print a header or footer for each screen iteration. Setting 'starting' to 'True' prints a header; prints a footer otherwise."""
    if starting:
        print(
            colored(f"\n[$] ", "blue", attrs=["bold"]),
            f"Begin Stage {stage} [",
            colored(f"{process}", "blue"),
            "]\n",
            sep="",
        )
    else:
        print(
            colored(f"\n[$] ", "blue", attrs=["bold"]),
            f"Stage {stage} [",
            colored(f"{process}", "blue"),
            "] Finished [",
            colored(f"{format_seconds(elapsed_time)}", "blue"),
            "]\n",
            sep="",
        )


def format_seconds(seconds: float) -> str:
    """Format a raw float value representing elapsed seconds into a printable string."""
    if seconds < 60:
        return f"{seconds:.2f} sec"
    else:
        minute_component = seconds // 60
        second_component = seconds % 60
        return f"{minute_component} min {second_component:.2f} sec"


def print_minimums(criteria: Dict[str, str], newline=True) -> None:
    """Print minimum values needed to pass screen iterations."""
    for key, value in criteria.items():
        print(
            colored(f"Minimum {key} to pass: ", "dark_grey"),
            colored(f"{value}", "light_grey"),
            sep="",
        )

    # add newline
    if newline:
        print()


def print_divider() -> None:
    cprint(
        "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
        "dark_grey",
    )


def skip_message(symbol: str, message: str) -> str:
    """Return a custom message logging screening errors."""
    return colored(f"\nSkipping {symbol} ({message}) . . .\n", "red")


def filter_message(symbol: str) -> str:
    """Return a custom message for logging when a stock is filtered out by a screen."""
    return colored(f"\n{symbol} filtered out.\n", "dark_grey")


def message(message: str) -> str:
    """Return a custom message for logging purposes."""
    return f"\n{message}\n"
