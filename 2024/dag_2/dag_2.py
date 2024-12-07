def read_input() -> list[list[int]]:
    """Read input from the input file.

    1. Open file
    2. Split the input
    3. Convert to integers
    4. Sort the lists
    """
    with open("2024/dag_2/input.txt") as f:
        lines = f.read().splitlines()

    reports = []
    for line in lines:
        reports.append([int(c) for c in line.split()])

    return reports


def is_safe_report(current_report: list[int]) -> bool:
    """Check if a report is safe.

    Rules:
    - The levels are either all increasing or all decreasing.
    - Any two adjacent levels differ by at least one and at most three.
    """
    increasing = None
    for i in range(1, len(current_report)):
        level_change = current_report[i] - current_report[i - 1]
        if increasing is None:
            increasing = level_change > 0

        # Check for neither an increase or a decrease
        if level_change == 0:
            return False

        # Check if levels are either all increasing or all decreasing
        if (increasing and level_change < 0) or (increasing is False and level_change > 0):
            return False

        # Check if levels differ by at most three
        if abs(level_change) > 3:
            return False

    return True


def is_safe_report_with_problem_dampener(report: list[int]) -> bool:
    """Tolerate a single bad level in the report."""
    if is_safe_report(report):
        return True

    # Check if the report is safe without any one of the levels in the report
    for i in range(len(report)):
        report_without_offending_value = report.copy()
        del report_without_offending_value[i]

        if is_safe_report(report_without_offending_value):
            return True

    return False


def main() -> None:
    """Main function for day 2."""
    reports = read_input()

    safe_reports = sum(is_safe_report(report) for report in reports)
    print(f"Safe reports (1): {safe_reports}")

    safe_reports = sum(is_safe_report_with_problem_dampener(report) for report in reports)
    print(f"Safe reports (2): {safe_reports}")


if __name__ == "__main__":
    main()
