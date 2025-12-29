import random
from pathlib import Path

import click
from matplotlib import path


def read_input(file_path: Path) -> list[list[int]]:
    with open(file_path) as f:
        return [
            [int(x) for x in line.split(",")]
            for line in f.read().splitlines()
        ]


def rectangle_other_corners(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (x1, y2), (x2, y1)


def calc_bounds(corners, step=10):
    xs = [x for x, y in corners]
    ys = [y for x, y in corners]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)

    boundary = []

    # bottom edge
    for x in range(xmin, xmax + 1, step):
        boundary.append((x, ymin))

    # right edge
    for y in range(ymin + step, ymax, step):
        boundary.append((xmax, y))

    # top edge
    for x in range(xmax, xmin - 1, -step):
        boundary.append((x, ymax))

    # left edge
    for y in range(ymax - step, ymin, -step):
        boundary.append((xmin, y))

    random.shuffle(boundary)
    return boundary

def within_bounds(poly_path, points: list[tuple[int, int]]) -> bool:
    for point in points:
        if not poly_path.contains_point(point, radius=1):
            return False
    return True

def solution(poly: list[list[int]]) -> None:
    poly_path = path.Path(poly + [poly[0]])

    largest_rectangle_area_p1 = 0
    largest_rectangle_area_p2 = 0
    for p1 in poly:
        for p2 in poly:
            if p1 == p2:
                continue
            x1, y1 = p1
            x2, y2 = p2
            rectangle_area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
            if rectangle_area > largest_rectangle_area_p1:
                largest_rectangle_area_p1 = rectangle_area
            if rectangle_area > largest_rectangle_area_p2:
                p3, p4 = rectangle_other_corners(p1, p2)
                corners = [p1, p2, p3, p4]
                if within_bounds(poly_path, corners):
                    if within_bounds(poly_path, calc_bounds(corners)):
                        print(f"Found largest rectangle area: {rectangle_area} with {p1} and {p2}")
                        largest_rectangle_area_p2 = rectangle_area

    print(f"Part 1: {largest_rectangle_area_p1}")
    print(f"Part 2: {largest_rectangle_area_p2}")

@click.command()
# test flag
@click.option("--test", is_flag=True, help="Run with test input")
def cli(test: bool) -> None:
    """CLI function."""
    file_path = Path(__file__).parent / ("example.txt" if test else "input.txt")
    puzzle_input = read_input(file_path)
    solution(puzzle_input)


if __name__ == "__main__":
    cli()
