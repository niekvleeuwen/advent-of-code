from dataclasses import dataclass
from enum import Enum
from math import prod
from typing import Counter

ROWS = 103
COLS = 101
CENTER_ROW = ROWS // 2
CENTER_COL = COLS // 2


class Quadrant(Enum):
    """Represents a quadrant."""

    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_LEFT = 3
    BOTTOM_RIGHT = 4


@dataclass
class Robot:
    """Represents a Robot."""

    position: tuple
    velocity: tuple

    @classmethod
    def parse(cls, input_str: str) -> "Robot":
        """Parse a string to a Robot object."""
        position, velocity = input_str.split()
        position = tuple([int(pos) for pos in position.lstrip("p=").split(",")])
        velocity = tuple([int(vel) for vel in velocity.lstrip("v=").split(",")])
        return Robot(position=position, velocity=velocity)

    def step(self) -> None:
        """Take a step from the current position to the new position based on the given velocity.

        For example with a grid of (11, 7) starting at (0,0):

        Robot p=2,4 v=2,-3
        Initial state: 2,4
        After 1 second: 4, 1
        After 2 seconds: 6, 5
        After 3 seconds: 8, 2
        After 4 seconds: 10, 6
        After 5 seconds: 1, 3
        """
        new_x = (self.position[0] + self.velocity[0]) % COLS
        new_y = (self.position[1] + self.velocity[1]) % ROWS
        self.position = (new_x, new_y)

    def get_quadrant(self) -> Quadrant | None:
        """Get quadrant using the current position."""
        x, y = self.position
        if x < CENTER_COL:
            if y < CENTER_ROW:
                return Quadrant.TOP_LEFT
            if y > CENTER_ROW:
                return Quadrant.BOTTOM_LEFT
        if x > CENTER_COL:
            if y < CENTER_ROW:
                return Quadrant.TOP_RIGHT
            if y > CENTER_ROW:
                return Quadrant.BOTTOM_RIGHT


def read_input() -> list[Robot]:
    """Read input.

    1. Open file
    2. Return a list with Machine objects
    """
    with open("dag_14/input.txt") as f:
        return [Robot.parse(input_str) for input_str in f.readlines()]


def print_state(robots: list[Robot]) -> None:
    """Print the state of the current robots."""
    robot_positions = [r.position for r in robots]
    for y in range(ROWS):
        for x in range(COLS):
            no_of_robots = robot_positions.count((x, y))
            print(no_of_robots or ".", end="")
        print()


def calculate_safety_factor(robots: list[Robot], no_of_steps: int) -> int:
    """Calculate the safety factor."""
    for _ in range(no_of_steps):
        for r in robots:
            r.step()

    quadrants = [r.get_quadrant() for r in robots]

    counts = Counter(filter(None, quadrants))

    return prod(counts.values())


def count_neighbors(robots: list[Robot]) -> int:
    """Count the number of neighbors for each point."""
    points = [r.position for r in robots]
    points_set = set(points)

    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    total = 0
    for x, y in points:
        total += sum((x + dx, y + dy) in points_set for dx, dy in directions)

    return total


def find_easter_egg(robots: list[Robot]) -> int:
    """Find easter egg in the outputs."""
    max_loop = 10000
    current_highest = 0
    current_highest_index = 0
    for i in range(max_loop):
        for r in robots:
            r.step()

        neighbors = count_neighbors(robots)
        if neighbors > current_highest:
            current_highest = neighbors
            current_highest_index = i + 1
            if neighbors > 500:
                print(f"Step {i + 1}: {neighbors} ({current_highest=})")
                print_state(robots)

    return current_highest_index


def main() -> None:
    """Main function for day 14."""
    robots = read_input()
    print("Safety factor (1):", calculate_safety_factor(robots, no_of_steps=100))
    robots = read_input()
    print("Easter egg (2):", find_easter_egg(robots))


if __name__ == "__main__":
    main()
