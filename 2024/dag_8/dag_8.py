import itertools
from collections import defaultdict
from typing import TypedDict


class Coordinate(TypedDict):
    """Represent a x,y coordinate."""

    x: int
    y: int


def read_input() -> list[list[str]]:
    """Read input.

    1. Open file
    2. Return puzzle as 2D array
    """
    with open("niek/dag_8/input.txt") as f:
        return [list(line) for line in f.read().splitlines()]


def find_frequencies_locations(array2d: list[list[str]]) -> dict[str, list[Coordinate]]:
    """Locate all antenna frequency coordinates."""
    sets = defaultdict(list)
    for y in range(len(array2d)):
        for x in range(len(array2d[0])):
            char = array2d[y][x]
            if char != ".":
                sets[char].append({"y": y, "x": x})
    return sets


def create_antinodes(array2d: list[list[str]], frequencies: dict) -> int:
    """Create antinodes for part 1."""
    antinodes_coordinates = []
    for antennas in frequencies.values():
        antenna_combinations = itertools.combinations(antennas, 2)
        for antenna_combination in antenna_combinations:
            for coordinate_1, coordinate_2 in itertools.permutations(antenna_combination, 2):
                new_coordinate = calc_antinode(coordinate_1, coordinate_2)

                if coordinate_in_bounds(array2d, new_coordinate):
                    antinodes_coordinates.append((new_coordinate["y"], new_coordinate["x"]))

    return len(list(set(antinodes_coordinates)))


def calc_antinode(coordinate: Coordinate, combined_coordinate: Coordinate) -> Coordinate:
    """Calculate an antinode for two coordinates."""
    y_diff = coordinate["y"] - combined_coordinate["y"]
    x_diff = coordinate["x"] - combined_coordinate["x"]

    return {
        "x": coordinate["x"] + x_diff,
        "y": coordinate["y"] + y_diff,
    }


def create_antinodes_resonant_harmonics(array2d: list[list[str]], frequencies: dict) -> int:
    """Create antinodes for part 2."""
    antinodes_coordinates = []
    for antennas in frequencies.values():
        antenna_combinations = itertools.combinations(antennas, 2)
        for antenna_combination in antenna_combinations:
            for coordinate_1, coordinate_2 in itertools.permutations(antenna_combination, 2):
                new_coordinate = calc_antinode(coordinate_1, coordinate_2)
                old_coordinate = coordinate_1

                antinodes_coordinates.append((coordinate_1["y"], coordinate_1["x"]))
                antinodes_coordinates.append((coordinate_2["y"], coordinate_2["x"]))

                while coordinate_in_bounds(array2d, new_coordinate):
                    antinodes_coordinates.append((new_coordinate["y"], new_coordinate["x"]))

                    old = new_coordinate
                    new_coordinate = calc_antinode(new_coordinate, old_coordinate)
                    old_coordinate = old

    return len(list(set(antinodes_coordinates)))


def coordinate_in_bounds(array2d: list[list[str]], coordinate: Coordinate) -> bool:
    """Check if a coordinate is in bounds."""
    max_y = len(array2d)
    max_x = len(array2d[0])
    return coordinate["x"] >= 0 and coordinate["x"] < max_x and coordinate["y"] >= 0 and coordinate["y"] < max_y


def main() -> None:
    """Main function for day 8."""
    array2d = read_input()

    frequencies = find_frequencies_locations(array2d)

    no_of_antinodes_part_1 = create_antinodes(array2d, frequencies)
    print(f"{no_of_antinodes_part_1=}")

    no_of_antinodes_part_2 = create_antinodes_resonant_harmonics(array2d, frequencies)
    print(f"{no_of_antinodes_part_2=}")


if __name__ == "__main__":
    main()
