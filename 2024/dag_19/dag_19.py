import functools


def read_input() -> tuple[tuple, list]:
    """Read input.

    1. Open file
    2. Split into the available towels and desired designs
    """
    with open("dag_19/input.txt") as f:
        available_towels, combinations = f.read().split("\n\n")
        available_towels = tuple(available_towels.split(", "))
        combinations = combinations.splitlines()
        return available_towels, combinations


@functools.cache
def count_possibilities(combination: str, available_towels: tuple[str]) -> int:
    """Count the possibilities in which this combination can be composed."""
    if not combination:
        return True

    possible_ways = 0
    for towel in available_towels:
        if combination.startswith(towel):
            # Strip the towel from the start of the combination
            left_part = combination[len(towel) :]
            # Recursively count the possibilities for the remainder
            possible_ways += count_possibilities(left_part, available_towels)

    return possible_ways


def main() -> None:
    """Main function for pattern validation."""
    available_towels, combinations = read_input()

    possible_combinations = 0
    unique_ways_to_create_combinations = 0

    for combination in combinations:
        if ways := count_possibilities(combination, available_towels):
            possible_combinations += 1
            unique_ways_to_create_combinations += ways

    print(f"Possible combinations: {possible_combinations}")
    print(f"Number of different ways to make each design: {unique_ways_to_create_combinations}")


if __name__ == "__main__":
    main()
