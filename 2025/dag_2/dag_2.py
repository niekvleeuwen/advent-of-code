def read_input() -> list[str]:
    with open("2025/dag_2/input.txt") as f:
        lines = f.read().split(",")
    return lines


def split_into_parts(s: str, x: int) -> list[str]:
    n = len(s)
    size = n // x
    return [s[i * size : (i + 1) * size] for i in range(x)]


def solution(ranges: list[str]) -> None:
    sum_of_invalid_ids_part_1 = 0
    sum_of_invalid_ids_part_2 = 0
    for r in ranges:
        start, stop = r.split("-")
        for value in range(int(start), int(stop) + 1):
            str_val = str(value)
            str_len = len(str_val)

            # Part 1: split into two parts if even
            if len(str_val) % 2 == 0:
                first_part, second_part = split_into_parts(str_val, 2)
                if first_part == second_part:
                    sum_of_invalid_ids_part_1 += value

            # Part 2: split into all possible divisors
            divisors = [d for d in range(2, str_len + 1) if str_len % d == 0]

            for d in divisors:
                parts = split_into_parts(str_val, d)

                # check if all parts are equal
                if parts.count(parts[0]) == len(parts):
                    sum_of_invalid_ids_part_2 += value
                    break

    print(f"Part 1: {sum_of_invalid_ids_part_1}")
    print(f"Part 2: {sum_of_invalid_ids_part_2}")


def main() -> None:
    """Main function for day 2."""
    ranges = read_input()
    print("Running...")
    solution(ranges)


if __name__ == "__main__":
    main()
