import re


def read_input() -> str:
    """Read input."""
    with open("dag_3/input.txt") as f:
        return f.read()


def parse_mul(instruction: str) -> int:
    """Parse and execute multiply instruction."""
    val_1, val_2 = instruction.lstrip("mul(").rstrip(")").split(",")
    return int(val_1) * int(val_2)


def part_1(instructions: str) -> int:
    """Search for `mul` operations and execute them."""
    total = 0
    for instruction in re.findall(r"mul\([0-9]+,[0-9]+\)", instructions):
        total += parse_mul(instruction)
    return total


def part_2(instructions: str) -> int:
    """Search for `mul` operations and execute them based on `do()` and `don't()` instructions."""
    total = 0
    currently_doing = True
    for instruction in re.findall(r"mul\([0-9]+,[0-9]+\)|don't\(\)|do\(\)", instructions):
        match instruction:
            case "don't()":
                currently_doing = False
            case "do()":
                currently_doing = True
            case _:
                if currently_doing:
                    total += parse_mul(instruction)
    return total


def main() -> None:
    """Main function for day 3."""
    instructions = read_input()

    print(f"Result (1): {part_1(instructions)}")
    print(f"Result (2): {part_2(instructions)}")


if __name__ == "__main__":
    main()
