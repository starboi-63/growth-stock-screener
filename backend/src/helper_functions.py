# calculate the percent change between two numbers
def percent_change(initial: float, final: float) -> float:
    return (final - initial) / initial


# calculate the raw relative strength of a stock given its price at the starts and ends of four trading quarters
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
    q1_change = percent_change(q1_start, q1_end)
    q2_change = percent_change(q2_start, q2_end)
    q3_change = percent_change(q3_start, q3_end)
    q4_change = percent_change(q4_start, q4_end)

    return 0.2(q1_change) + 0.2(q2_change) + 0.2(q3_change) + 0.4(q4_change)
