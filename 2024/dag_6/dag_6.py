from copy import deepcopy
from enum import Enum

PRINT = False


class StuckInLoopError(Exception):
    """Raised of the guard is stuck in a loop."""

    pass


class NoStartPositionFoundError(Exception):
    """Raised if puzzle misses a start position for the guard."""

    pass


class Direction(Enum):
    """Indicates the direction that the guard is facing."""

    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

    def next_direction(self) -> "Direction":
        """Next direction assuming a 90 degree turn."""
        v = self.value + 1
        if v > 4:
            v = 1
        return Direction(v)


def read_input() -> list[list[str]]:
    """Read input.

    1. Open file
    2. Return puzzle as 2D array
    """
    with open("dag_6/input.txt") as f:
        return [list(line) for line in f.read().splitlines()]


class RouteTracer:
    """Class responsible for tracing the route of the guard."""

    def __init__(self, puzzle: list[list[str]]) -> None:
        self.puzzle = puzzle
        self.len_y = len(puzzle)
        self.len_x = len(puzzle[0])
        self.start_position = self.retrieve_start_position()
        self.current_position = self.start_position
        self.current_direction = Direction.UP

    def trace_route(self, return_unique_coordinates: bool = False) -> list[tuple] | None:
        """Trace the route of the guard."""
        inside_area = True
        positions_visited = []
        steps_taken = 0
        while inside_area:
            positions_visited.append(self.current_position)

            if self.next_position_outside_area():
                self.print("Outside area, exiting.")
                inside_area = False
                break
            elif self.check_if_in_loop(steps_taken):
                raise StuckInLoopError

            if self.something_directly_in_front():
                self.print("Found something in front, turning 90 degrees.")
                self.turn_90_degrees()
            else:
                self.take_step_forward()
                steps_taken += 1

        if return_unique_coordinates:
            unique_coordinates = []
            for coordinate in positions_visited:
                if coordinate not in unique_coordinates:
                    unique_coordinates.append(coordinate)

            if PRINT:
                self.print_grid(unique_coordinates)
            return unique_coordinates
        return

    def retrieve_start_position(self) -> tuple:
        """Retrieve the starting position from the puzzle."""
        y, x = 0, 0
        for y in range(self.len_y):
            for x in range(self.len_x):
                char = self.puzzle[y][x]
                if char == "^":  # Assume starting position is up
                    self.puzzle[y][x] = "."
                    return y, x
        raise NoStartPositionFoundError("No start position found!")

    def next_position(self) -> tuple:
        """Calculate the next position based on the direction."""
        y, x = self.current_position

        match self.current_direction:
            case Direction.UP:
                y -= 1
            case Direction.DOWN:
                y += 1
            case Direction.RIGHT:
                x += 1
            case Direction.LEFT:
                x -= 1
            case _:
                raise ValueError("Incorrect direction.")
        return y, x

    def something_directly_in_front(self) -> bool:
        """Check if there is something directly in front of the guard."""
        next_position = self.next_position()
        return self.char_for_coordinate(next_position) != "."

    def turn_90_degrees(self) -> None:
        """Turn the guard 90 degrees."""
        self.current_direction = self.current_direction.next_direction()

    def take_step_forward(self) -> None:
        """Take a step forward."""
        next_position = self.next_position()
        self.print(f"Taking step forward from {self.current_position} to {next_position}")
        self.current_position = next_position

    def check_if_in_loop(self, steps_taken: int) -> bool:
        """Check if the guard is stuck in a loop.

        Assumes that the guard is stuck if more steps staken than half of all the available positions.
        """
        return steps_taken > (self.len_y * self.len_x / 2)

    def char_for_coordinate(self, coordinate: tuple) -> str:
        """Retrieve the character at the given coordinate."""
        y, x = coordinate
        return self.puzzle[y][x]

    def next_position_outside_area(self) -> bool:
        """Check if next position is inside the safe area."""
        y, x = self.next_position()
        return x < 0 or x >= self.len_x or y < 0 or y >= self.len_y

    def print(self, string: str) -> None:
        """Utility function."""
        if PRINT:
            print(string)

    def print_grid(self, unique_coordinates: list[tuple]) -> None:
        """Print the grid with a set of coordinates."""
        for y in range(self.len_y):
            for x in range(self.len_x):
                if (y, x) in unique_coordinates:
                    print("X", end="")
                else:
                    print(self.char_for_coordinate((y, x)), end="")
            print()


def main() -> None:
    """Main function for day 6."""
    original_puzzle = read_input()

    puzzle = deepcopy(original_puzzle)

    route_tracer = RouteTracer(puzzle)
    unique_positions_visited = route_tracer.trace_route(return_unique_coordinates=True)
    if not unique_positions_visited:
        return

    possible_obstacle_positions = 0
    for i, coordinate in enumerate(unique_positions_visited, start=1):
        print(f"{i}/{len(unique_positions_visited)}: placing obstacle at {coordinate}")
        puzzle_with_obstacle = deepcopy(original_puzzle)
        y, x = coordinate
        puzzle_with_obstacle[y][x] = "O"

        try:
            route_tracer = RouteTracer(puzzle_with_obstacle)
        except NoStartPositionFoundError:
            # Skip puzzle with obstacle at start position
            continue

        try:
            route_tracer.trace_route()
        except StuckInLoopError:
            possible_obstacle_positions += 1

    print(f"Unique positions visited: {len(unique_positions_visited)}")
    print(f"Possible obstacle positions: {possible_obstacle_positions}")


if __name__ == "__main__":
    main()
