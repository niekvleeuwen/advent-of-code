from typing import Tuple


def read_input() -> Tuple[list, list]:
    """Read input from the input file.

    1. Open file
    2. Split the input
    3. Convert to integers
    4. Sort the lists
    """
    with open("2024/dag_1/input.txt") as f:
        lines = f.read().splitlines()

    list_1, list_2 = [], []
    for line in lines:
        val_1, val_2 = line.split()
        list_1.append(int(val_1))
        list_2.append(int(val_2))

    list_1.sort()
    list_2.sort()

    return list_1, list_2


def part_1(list_1: list, list_2: list) -> int:
    """Calculate the distance between the values in both lists."""
    return sum([abs(val_1 - val_2) for val_1, val_2 in zip(list_1, list_2)])


def part_2(list_1: list, list_2: list) -> int:
    """Multiply the value in list 1 with the number of occurrences in list 2."""
    total_distance = 0
    for val_1 in list_1:
        occurrences = list_2.count(val_1)
        distance = occurrences * val_1
        total_distance += distance
    return total_distance


def main() -> None:
    """Main function for day 1."""
    list_1, list_2 = read_input()

    print(f"Total distance (1): {part_1(list_1, list_2)}")
    print(f"Total distance (2): {part_2(list_1, list_2)}")


if __name__ == "__main__":
    main()
