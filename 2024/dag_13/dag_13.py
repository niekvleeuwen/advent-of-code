from dataclasses import dataclass

from sympy import Eq, solve, symbols

COST_BUTTON_A = 3
COST_BUTTON_B = 1


@dataclass
class Machine:
    """Represent a Machine."""

    button_a: tuple[int, int]
    button_b: tuple[int, int]
    prize: tuple[int, int]

    @classmethod
    def parse(cls, input_str: str) -> "Machine":
        """Parse the input string to a Machine object."""

        def parse_button_translation(button_str: str) -> tuple[int, int]:
            btn = button_str.replace("X+", "").replace("Y+", "").strip().split(",")
            btn = int(btn[0]), int(btn[1])
            return btn

        lines = [line.split(":")[-1] for line in input_str.splitlines()]
        button_a, button_b, prize = lines
        button_a = parse_button_translation(button_a)
        button_b = parse_button_translation(button_b)
        prize = prize.replace("X=", "").replace("Y=", "").strip().split(",")
        prize = int(prize[0]), int(prize[1])
        return Machine(button_a, button_b, prize)

    def cheapest_way_to_win(self) -> int:
        """Calculate the cheapest way to win the machine."""
        solutions = self.solve()

        cheapest_solution = None
        for solution in solutions:
            cost = (solution[0] * COST_BUTTON_A) + (solution[1] * COST_BUTTON_B)
            if cheapest_solution is None or cheapest_solution > cost:
                cheapest_solution = cost
        return cheapest_solution or 0

    def solve(self) -> list[tuple[int, int]]:
        """Solve the equation for the machine.

        For example:

        Button A: X+94, Y+34
        Button B: X+22, Y+67
        Prize: X=8400, Y=5400

        94x + 34y = 8400
        34x + 40y = 5400

        Returns:
            list of tuples: list of integer solutions

        """
        btnAX, btnAY = self.button_a
        btnBX, btnBY = self.button_b
        prizeX, prizeY = self.prize

        x, y = symbols("x y", integer=True)
        eq1 = Eq(btnAX * x + btnBX * y, prizeX)
        eq2 = Eq(btnAY * x + btnBY * y, prizeY)
        return [(sol[x], sol[y]) for sol in solve((eq1, eq2), (x, y), dict=True)]


def read_input() -> list[Machine]:
    """Read input.

    1. Open file
    2. Return a list with Machine objects
    """
    with open("dag_13/input.txt") as f:
        return [Machine.parse(machine_str) for machine_str in f.read().split("\n\n")]


def main() -> None:
    """Main function for day 13."""
    machines = read_input()

    total_1 = sum([machine.cheapest_way_to_win() for machine in machines])

    # Adapt input for part 2
    for machine in machines:
        prize_x, prize_y = machine.prize
        machine.prize = (prize_x + 10000000000000, prize_y + 10000000000000)

    total_2 = sum([machine.cheapest_way_to_win() for machine in machines])

    print(f"Tokens (1): {total_1}")
    print(f"Tokens (2): {total_2}")


if __name__ == "__main__":
    main()
