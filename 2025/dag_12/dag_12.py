from dataclasses import dataclass
from pathlib import Path
from typing import List

import click


@dataclass
class Shape:
    pattern: list[list[str]]
    filled_count: int = 0

    def __post_init__(self) -> None:
        self.filled_count = sum(1 for row in self.pattern for cell in row if cell == "#")


@dataclass
class Region:
    x: int
    y: int
    # 1 0 1 0 3 2 means
    # shape 0 present 1 time
    # shape 1 present 0 times
    # shape 2 present 1 time
    # shape 3 present 0 times
    # shape 4 present 3 times
    # shape 5 present 2 times
    present_shapes: list[int]


def read_input(file_path: Path) -> tuple[list[Shape], list[Region]]:
    """Read input."""
    with open(file_path) as f:
        lines = [line for line in f.read().splitlines()]
    shapes = []
    regions = []

    index = 0
    while index < len(lines):
        line = lines[index]
        if line == "":
            index += 1
        elif "x" not in line:
            shape = []
            index += 1
            for _ in range(3):
                shape.append(list(lines[index]))
                index += 1
            shapes.append(Shape(pattern=shape))
        else:
            splitted = line.split(": ")
            region = Region(
                x=int(splitted[0].split("x")[0]),
                y=int(splitted[0].split("x")[1]),
                present_shapes=[int(x) for x in splitted[1].split()],
            )
            regions.append(region)
            index += 1
    return [shapes, regions]


def region_can_fit_all_shapes(region: Region, shapes: List[Shape]) -> bool:
    required_cells = sum(count * shape.filled_count for count, shape in zip(region.present_shapes, shapes))
    available_cells = region.x * region.y
    return required_cells <= available_cells


@click.command()
# test flag
@click.option("--test", is_flag=True, help="Run with test input")
def cli(test: bool) -> None:
    """CLI function."""
    file_path = Path(__file__).parent / ("example.txt" if test else "input.txt")
    shapes, regions = read_input(file_path)
    result = sum(region_can_fit_all_shapes(region, shapes) for region in regions)
    print(f"Result: {result}")


if __name__ == "__main__":
    cli()
