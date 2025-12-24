from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

import click
from ortools.sat.python import cp_model


@dataclass
class Machine:
    target: list[bool]
    buttons: list[tuple[int, ...]]
    joltage: tuple[int, ...]
    state: list[bool]

    @classmethod
    def parse_from_string(cls, val: str) -> "Machine":
        """Parse Machine from string.

        For example, parse "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
        """
        parts = val.split()
        target_str = parts[0][1:-1]  # Remove brackets
        target = [c == "#" for c in target_str]
        state = [False] * len(target)

        buttons = []
        for part in parts[1:-1]:
            btn_str = part[1:-1]  # Remove parentheses
            btn = tuple(int(x) for x in btn_str.split(","))
            buttons.append(btn)

        joltage_str = parts[-1][1:-1]  # Remove curly braces
        joltage = tuple(int(x) for x in joltage_str.split(","))

        return Machine(target=target, buttons=buttons, joltage=joltage, state=state)


def read_input(file_path: Path) -> list[list[str]]:
    """Read input."""
    with open(file_path) as f:
        return [Machine.parse_from_string(line) for line in f.read().splitlines()]


def configure_indicator_light(machine: Machine) -> int:
    """Small search space so instant brute-force."""
    n = len(machine.target)
    m = len(machine.buttons)

    # Convert initial and target states to bitmasks
    init_mask = 0
    target_mask = 0
    for i in range(n):
        if machine.state[i]:
            init_mask |= 1 << i
        if machine.target[i]:
            target_mask |= 1 << i

    # Precompute each button as a bitmask
    button_masks: list[int] = []
    for btn in machine.buttons:
        mask = 0
        for idx in btn:
            mask ^= 1 << idx
        button_masks.append(mask)

    # Brute-force all combinations of button presses
    for k in range(m + 1):
        for combo in combinations(range(m), k):
            flip_mask = 0
            for j in combo:
                flip_mask ^= button_masks[j]

            if init_mask ^ flip_mask == target_mask:
                return k

    raise ValueError("Target state is unreachable")


def solve_min_presses_joltage(machine: Machine) -> int:
    """Solve the machine using integer optimization instead of brute-force or search."""
    target = list(machine.joltage)
    n = len(target)
    m = len(machine.buttons)

    # Build matrix
    A = [[0] * m for _ in range(n)]
    for j, btn in enumerate(machine.buttons):
        for i in set(btn):
            A[i][j] = 1

    model = cp_model.CpModel()

    # Upper bound
    ub = max(target)
    x = [model.NewIntVar(0, ub, f"x{j}") for j in range(m)]

    # Equality constraints per index
    for i in range(n):
        model.Add(sum(A[i][j] * x[j] for j in range(m)) == target[i])

    # Minimize total presses
    model.Minimize(sum(x))

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 16  # Go fast

    solver.Solve(model)

    return sum([solver.Value(v) for v in x])


@click.command()
# test flag
@click.option("--test", is_flag=True, help="Run with test input")
def cli(test: bool) -> None:
    """CLI function."""
    file_path = Path(__file__).parent / ("example.txt" if test else "input.txt")
    puzzle_input = read_input(file_path)
    print(f"Part 1: {sum([configure_indicator_light(machine) for machine in puzzle_input])}")
    print(f"Part 2: {sum([solve_min_presses_joltage(machine) for machine in puzzle_input])}")


if __name__ == "__main__":
    cli()
