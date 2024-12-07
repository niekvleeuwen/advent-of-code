import itertools
from dataclasses import dataclass

OPERATORS_PART_1 = ["+", "*"]
OPERATORS_PART_2 = ["+", "*", "||"]


@dataclass
class Equation:
    """Represents an equation."""

    values: list[int]
    result: int

    @classmethod
    def parse(cls, input_str: str) -> "Equation":
        """Parse string to class."""
        result, values = input_str.split(":")
        return Equation(values=[int(val) for val in values.strip().split(" ")], result=int(result))

    def evaluate(self, operators: tuple) -> bool:
        """Check if given operators equal to specified result."""
        value = self.values[0]
        for i, operator in enumerate(operators, start=1):
            if operator == "*":
                value *= self.values[i]
            if operator == "+":
                value += self.values[i]
            if operator == "||":
                value = int(str(value) + str(self.values[i]))

        return value == self.result


def read_input() -> list[Equation]:
    """Read input.

    1. Open file
    2. Parse each equation
    """
    with open("niek/dag_7/input.txt") as f:
        return [Equation.parse(input_str) for input_str in f.read().splitlines()]


def is_solvable(eq: Equation, available_operators: list) -> bool:
    """Check if an equation is solvable."""
    no_of_operator_positions = len(eq.values) - 1
    operator_combinations = itertools.product(available_operators, repeat=no_of_operator_positions)
    for operators in operator_combinations:
        if eq.evaluate(operators):
            return True
    return False


def main() -> None:
    """Main function for day 5."""
    equations = read_input()

    part_1 = sum([eq.result for eq in equations if is_solvable(eq, OPERATORS_PART_1)])
    print(f"Result (1): {part_1}")

    part_2 = sum([eq.result for eq in equations if is_solvable(eq, OPERATORS_PART_2)])
    print(f"Result (2): {part_2}")


if __name__ == "__main__":
    main()
