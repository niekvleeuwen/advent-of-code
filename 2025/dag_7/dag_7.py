from functools import lru_cache
from pathlib import Path
from typing import Generator

import click


def read_input(file_path: Path) -> list[list[str]]:
    """Read input."""
    with open(file_path) as f:
        return [list(line) for line in f.read().splitlines()]


def part_1(puzzle_input: list[list[str]]) -> int:
    start_pos = (0, puzzle_input[0].index("S"))
    rows, cols = len(puzzle_input), len(puzzle_input[0])

    current_beams_cols = [start_pos[1]]
    total_times_splitted = 0

    # Move downwards from the start position
    for i in range(1, rows):
        # for every beam col, check if reach splitter (^) or empty space (.)
        beams_to_check = current_beams_cols.copy()
        for beam_col in beams_to_check:
            cell = puzzle_input[i][beam_col]
            # beam continues downwards
            if cell == ".":
                puzzle_input[i][beam_col] = "|"
            # beam reaches splitter
            elif cell == "^":
                # split beam to left and right
                if beam_col - 1 >= 0 and (beam_col - 1) not in current_beams_cols:
                    current_beams_cols.append(beam_col - 1)
                    puzzle_input[i][beam_col - 1] = "|"
                if beam_col + 1 < cols and (beam_col + 1) not in current_beams_cols:
                    current_beams_cols.append(beam_col + 1)
                    puzzle_input[i][beam_col + 1] = "|"

                # Remove current beam as it splits
                current_beams_cols.remove(beam_col)

                total_times_splitted += 1

    return total_times_splitted


def part_2(puzzle_input: list[list[str]]) -> int:
    rows, cols = len(puzzle_input), len(puzzle_input[0])

    def neighbors(r: int, c: int) -> Generator:
        nr = r + 1
        if nr >= rows:
            # No valid neighbors beyond last row
            return

        # Continue vertically down if beam
        if puzzle_input[nr][c] == "|":
            yield nr, c

        # If splitter, track down left and right
        if puzzle_input[nr][c] == "^":
            if c - 1 >= 0 and puzzle_input[nr][c - 1] == "|":
                yield nr, c - 1
            if c + 1 < cols and puzzle_input[nr][c + 1] == "|":
                yield nr, c + 1

    @lru_cache(maxsize=None)
    def dfs(r: int, c: int) -> int:
        # Add valid path if reached bottom row
        if r == rows - 1:
            return 1

        total = 0
        for nr, nc in neighbors(r, c):
            total += dfs(nr, nc)
        return total

    start_col = puzzle_input[0].index("S")
    return dfs(0, start_col)


@click.command()
@click.option("--test", is_flag=True, help="Run with test input")
def cli(test: bool) -> None:
    """CLI function."""
    file_path = Path(__file__).parent / ("example.txt" if test else "input.txt")
    puzzle_input = read_input(file_path)
    print(f"Part 1: {part_1(puzzle_input)}")
    print(f"Part 2: {part_2(puzzle_input)}")


if __name__ == "__main__":
    cli()
