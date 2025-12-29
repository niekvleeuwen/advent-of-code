def read_input() -> list[list]:
    with open("niek/2025/dag_3/input.txt") as f:
        lines = f.read().splitlines()

    result = []
    for line in lines:
        battery_bank = []
        for char in line:
            battery_bank.append(int(char))
        result.append(battery_bank)
    return result


def max_joltage(batteries: list[int], no_of_batteries: int = 12) -> int:
    pos = 0
    result = []

    for picked in range(no_of_batteries):
        spaces_left = no_of_batteries - picked
        last_option = len(batteries) - spaces_left

        best_digit = 0
        best_idx = pos

        for i in range(pos, last_option + 1):
            if batteries[i] > best_digit:
                best_digit = batteries[i]
                best_idx = i

        result.append(str(best_digit))
        pos = best_idx + 1

    return int("".join(result))


def main() -> None:
    """Main function for day 3."""
    battery_banks = read_input()
    p1 = 0
    p2 = 0
    for battery_bank in battery_banks:
        p1 += max_joltage(battery_bank, no_of_batteries=2)
        p2 += max_joltage(battery_bank, no_of_batteries=12)
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
