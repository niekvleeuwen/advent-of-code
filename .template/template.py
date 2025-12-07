from pathlib import Path

import click


def read_input(file_path: Path) -> list[list[str]]:
    """Read input."""
    with open(file_path) as f:
        return [line for line in f.read().splitlines()]


def solution(puzzle_input: list[list[str]]) -> int:
    """Solution function."""
    # Implement solution logic here
    print(puzzle_input)
    return 0


@click.command()
# test flag
@click.option("--test", is_flag=True, help="Run with test input")
def cli(test: bool) -> None:
    """CLI function."""
    file_path = Path(__file__).parent / ("example.txt" if test else "input.txt")
    puzzle_input = read_input(file_path)
    result = solution(puzzle_input)
    print(f"Result: {result}")


if __name__ == "__main__":
    cli()
