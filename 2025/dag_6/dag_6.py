import math


def read_input() -> list[str]:
    with open("2025/dag_6/input.txt") as f:
        return f.read().splitlines()


def apply_operator(operator: str, values: list[int]) -> int:
    if operator == "+":
        return sum(values)
    if operator == "*":
        return math.prod(values)
    raise ValueError("Invalid operator")


def part_1(lines: list[str]) -> int:
    lines = [line.split() for line in lines]
    values = lines[:-1]
    operators = lines[-1]

    total = 0
    no_of_vals = len(values)
    for i, operator in enumerate(operators):
        col = []
        for j in range(no_of_vals):
            col.append(int(values[j][i]))

        total += apply_operator(operator, col)
    return total


def part_2(lines: list[str]) -> int:
    lines = [list(line) for line in lines]
    values = lines[:-1]
    operators = [o for o in lines[-1] if o != " "]

    no_of_cols = max([len(r) for r in values])
    no_of_rows = len(values)

    current_col = []
    total = 0
    for j in range(no_of_cols - 1, -1, -1):
        values_in_col = []
        for i in range(no_of_rows):
            # check if index exists and not empty
            if j < len(values[i]) and values[i][j] != " ":
                values_in_col.append(values[i][j])

        if values_in_col:
            current_col.append(int("".join(values_in_col)))

        if not values_in_col or j == 0:
            total += apply_operator(operators.pop(), current_col)
            current_col = []

    return total


def main() -> None:
    """Main function for day 6."""
    lines = read_input()
    print(f"Part 1: {part_1(lines)}")
    print(f"Part 2: {part_2(lines)}")


if __name__ == "__main__":
    main()
