from dataclasses import dataclass
from typing import Self


@dataclass
class Rotation:
    direction: str
    no_of_rotations: int

    @classmethod
    def from_string(cls, val: str) -> Self:
        direction = val[0]
        no_of_rotations = int(val[1:])
        return cls(direction, no_of_rotations)

    def rotate(self, current_position: int, steps: int = 1) -> int:
        if self.direction == "L":
            return (current_position - steps) % 100

        elif self.direction == "R":
            return (current_position + steps) % 100

        raise ValueError


def read_input() -> list[Rotation]:
    with open("2025/dag_1/input.txt") as f:
        lines = f.read().splitlines()

    return [Rotation.from_string(s) for s in lines]


def part_1(rotations: list[Rotation]) -> None:
    dail = 50
    pointing_at_zero = 0
    for rotation in rotations:
        dail = rotation.rotate(dail, steps=rotation.no_of_rotations)
        if dail == 0:
            pointing_at_zero += 1

    print(f"Part 1: {pointing_at_zero}")


def part_2(rotations: list[Rotation]) -> None:
    dail = 50
    pointing_at_zero = 0
    for rotation in rotations:
        for _ in range(rotation.no_of_rotations):
            dail = rotation.rotate(dail)
            if dail == 0:
                pointing_at_zero += 1

    print(f"Part 2: {pointing_at_zero}")


def main() -> None:
    """Main function for day 1."""
    rotations = read_input()
    part_1(rotations)
    part_2(rotations)


if __name__ == "__main__":
    main()
