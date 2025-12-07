import math


def read_input() -> dict[int, int]:
    """Read input.

    1. Open file
    2. Return a dict with the stone numbers and number of occurrences.
    """
    with open("dag_11/input.txt") as f:
        stones = [int(stone) for stone in f.read().split(" ")]
        # Keep track of unique stone numbers and how many times the number occurs
        return {stone: stones.count(stone) for stone in stones}


def calculate_number_of_stones(stones: dict[int, int], no_of_blinks: int) -> int:
    """Calculate the number of stones after a given number of blinks."""
    for _ in range(no_of_blinks):
        new_stones = {}

        for stone, number_of_stones in stones.items():
            # If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
            if stone == 0:
                new_stones[1] = number_of_stones + new_stones.get(1, 0)
                continue

            # If the stone is engraved with a number that has an even number of digits, it is replaced by two stones.
            # The left half of the digits are engraved on the new left stone, and the right half of the digits are
            # engraved on the new right stone.
            number_of_digits = int(math.log10(stone)) + 1
            if number_of_digits % 2 == 0:
                n1 = int(10 ** (number_of_digits / 2))
                left = stone // n1
                right = stone % n1
                new_stones[left] = number_of_stones + new_stones.get(left, 0)
                new_stones[right] = number_of_stones + new_stones.get(right, 0)
                continue

            # If none of the other rules apply, the stone is replaced by a new stone; the old stone's number
            # multiplied by 2024 is engraved on the new stone.
            new_stone = stone * 2024
            new_stones[new_stone] = number_of_stones + new_stones.get(new_stone, 0)

        stones = new_stones

    return sum(n for n in stones.values())


def main() -> None:
    """Main function for day 11."""
    stones = read_input()

    print(f"Number of stones (25): {calculate_number_of_stones(stones, no_of_blinks=25)}")
    print(f"Number of stones (75): {calculate_number_of_stones(stones, no_of_blinks=75)}")


if __name__ == "__main__":
    main()
