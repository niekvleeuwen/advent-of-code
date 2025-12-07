SEARCH_PART_1 = ("XMAS", "SAMX")
SEARCH_PART_2 = ("MAS", "SAM")


def read_input() -> list[list[str]]:
    """Read input as a 2D vector list."""
    with open("dag_4/input.txt") as f:
        lines = f.read().splitlines()

    return [list(line) for line in lines]


def check_for_coordinates(
    puzzle: list[list[str]],
    coordinates: tuple,
    search: tuple[str, str],
) -> bool:
    """Check if a set of coordinates contain one of the given search words."""
    try:
        if any(x < 0 or y < 0 for x, y in coordinates):
            return False
        result = "".join([puzzle[y][x] for y, x in coordinates])
    except IndexError:
        return False

    return result in search


def part_1(puzzle: list[list[str]]) -> int:
    """Find the search words in the puzzle."""
    x, y = 0, 0
    len_x = len(puzzle[0])
    len_y = len(puzzle)

    coordinates_used = []
    for y in range(len_y):
        for x in range(len_x):
            horizontal = (y, x), (y, x + 1), (y, x + 2), (y, x + 3)
            vertical = (y, x), (y + 1, x), (y + 2, x), (y + 3, x)
            diagonal_right_up = (y, x), (y - 1, x + 1), (y - 2, x + 2), (y - 3, x + 3)
            diagonal_right_down = (y, x), (y + 1, x + 1), (y + 2, x + 2), (y + 3, x + 3)
            diagonal_left_up = (y, x), (y + 1, x - 1), (y + 2, x - 2), (y + 3, x - 3)
            diagonal_left_down = (y, x), (y - 1, x - 1), (y - 2, x - 2), (y - 3, x - 3)

            coordinate_rules = [
                horizontal,
                vertical,
                diagonal_right_up,
                diagonal_right_down,
                diagonal_left_up,
                diagonal_left_down,
            ]
            for coordinates in coordinate_rules:
                if check_for_coordinates(puzzle, coordinates, SEARCH_PART_1):
                    coordinates_used.append(coordinates)

    unique_coordinate_sets = list(map(list, {tuple(sorted(sublist)) for sublist in coordinates_used}))
    return len(unique_coordinate_sets)


def part_2(puzzle: list[list[str]]) -> int:
    """Find the search words in the puzzle."""
    x, y = 0, 0
    len_x = len(puzzle[0])
    len_y = len(puzzle)

    total = 0
    for y in range(len_y):
        for x in range(len_x):
            char = puzzle[y][x]
            if char == SEARCH_PART_2[0][1]:
                diagonal_left_to_right_up = (y - 1, x - 1), (y, x), (y + 1, x + 1)
                diagonal_left_to_right_down = (y + 1, x - 1), (y, x), (y - 1, x + 1)

                rules = [diagonal_left_to_right_down, diagonal_left_to_right_up]
                if all(check_for_coordinates(puzzle, rule, SEARCH_PART_2) for rule in rules):
                    total += 1

    return total


def main() -> None:
    """Main function for day 4."""
    puzzle = read_input()

    print(f"Result (1): {part_1(puzzle)}")
    print(f"Result (2): {part_2(puzzle)}")


if __name__ == "__main__":
    main()
