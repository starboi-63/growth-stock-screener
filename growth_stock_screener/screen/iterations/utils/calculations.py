import pandas as pd


def percent_change(initial: float, final: float) -> float:
    """Calculate the percent change between two positive numbers."""
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
    """Calculate the raw relative strength of a stock given its price at the starts and ends of four trading quarters."""
    q1_change = percent_change(q1_start, q1_end)
    q2_change = percent_change(q2_start, q2_end)
    q3_change = percent_change(q3_start, q3_end)
    q4_change = percent_change(q4_start, q4_end)

    return 0.2 * (q1_change) + 0.2 * (q2_change) + 0.2 * (q3_change) + 0.4 * (q4_change)
