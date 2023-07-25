import pandas as pd
import os


def percent_change(initial: float, final: float) -> float:
    """calculate the percent change between two positive numbers"""
    if initial == 0:
        raise ZeroDivisionError("Initial value of zero is undefined!")

    if pd.isna(initial) or pd.isna(final):
        raise ValueError("NaN inputs are undefined!")

    return 100 * (final - initial) / initial


def relative_strength(
    q1_start: float,
    q1_end: float,
    q2_start: float,
    q2_end: float,
    q3_start: float,
    q3_end: float,
    q4_start: float,
    q4_end: float,
) -> float:
    """calculate the raw relative strength of a stock given its price at the starts and ends of four trading quarters"""
    q1_change = percent_change(q1_start, q1_end)
    q2_change = percent_change(q2_start, q2_end)
    q3_change = percent_change(q3_start, q3_end)
    q4_change = percent_change(q4_start, q4_end)

    return 0.2 * (q1_change) + 0.2 * (q2_change) + 0.2 * (q3_change) + 0.4 * (q4_change)


def print_status(process: str, stage: int, starting: bool):
    """print a header or footer for each screen iteration"""
    if starting:
        print(f"\n****** Begin Stage {stage} [{process}] ******\n")
    else:
        print(f"\n****** Stage {stage} [{process}] Finished ******\n")


def print_skip(symbol: str, message: str):
    """print a custom message when screening a stock fails"""
    print(f"Skipping {symbol} ({message}) . . .\n")


def create_outfile(data: pd.DataFrame, filename: str):
    """serialize data in JSON format and save on machine"""
    serialized_json = data.to_json()
    outfile_path = os.path.join(os.getcwd(), "backend", "json", f"{filename}.json")

    with open(outfile_path, "w") as outfile:
        outfile.write(serialized_json)
