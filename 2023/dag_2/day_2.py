from dataclasses import dataclass, field


@dataclass
class Game:
    """Represents a game."""

    game_id: int
    red_values: list[int] = field(default_factory=lambda: [])
    green_values: list[int] = field(default_factory=lambda: [])
    blue_values: list[int] = field(default_factory=lambda: [])

    @classmethod
    def parse(cls, input_str: str) -> "Game":
        """Parse a string to a Game object."""
        game_id, reveals = input_str.split(":")
        game_id = int(game_id.split(" ")[-1])

        game = Game(game_id=game_id)

        for reveal in reveals.strip().split(";"):
            colors_shown = reveal.split(",")
            for color_shown in colors_shown:
                number, color = color_shown.strip().split(" ")
                number = int(number)
                match color:
                    case "red":
                        game.red_values.append(number)
                    case "green":
                        game.green_values.append(number)
                    case "blue":
                        game.blue_values.append(number)
                    case _:
                        raise ValueError("Unknown color")
        return game

    def is_possible(self, red: int, green: int, blue: int) -> bool:
        """Check if the game is possible given the number of red, green and blue cubes."""
        return max(self.red_values) <= red and max(self.green_values) <= green and max(self.blue_values) <= blue

    def power(self) -> int:
        """Returns the power of the cubes."""
        return max(self.red_values) * max(self.blue_values) * max(self.green_values)


def read_input() -> list[Game]:
    """Read input."""
    with open("2023/dag_2/input.txt") as f:
        return [Game.parse(input_str) for input_str in f.read().splitlines()]


def main() -> None:
    """Main function for day 1."""
    games = read_input()

    red_cubes_available = 12
    green_cubes_available = 13
    blue_cubes_available = 14
    part_1 = sum(
        [
            game.game_id
            for game in games
            if game.is_possible(red_cubes_available, green_cubes_available, blue_cubes_available)
        ]
    )
    print(f"Answer (1): {part_1}")

    part_2 = sum([game.power() for game in games])
    print(f"Answer (2): {part_2}")


if __name__ == "__main__":
    main()
