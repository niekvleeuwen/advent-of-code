def read_input() -> list[str]:
    """Read input."""
    with open("2023/dag_1/input.txt") as f:
        lines = f.read().splitlines()
    return lines


def part_1(line: str) -> int:
    """Combine the first digit and the last digit."""
    digits = [char for char in line if char.isdigit()]
    return int(digits[0] + digits[-1])


def part_2(line: str) -> int:
    """Convert spelled out letters into digits."""
    digits = []
    for i, c in enumerate(line):
        if c.isdigit():
            digits.append(c)
        for d, val in enumerate(["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"], start=1):
            if line[i:].startswith(val):
                digits.append(str(d))
    return int(digits[0] + digits[-1])


def main() -> None:
    """Main function for day 1."""
    lines = read_input()

    print(f"Answer (1): {sum([part_1(line) for line in lines ])}")
    print(f"Answer (2): {sum([part_2(line) for line in lines ])}")


if __name__ == "__main__":
    main()
