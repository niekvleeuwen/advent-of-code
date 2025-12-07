def read_input() -> list[list[str]]:
    with open("2025/dag_4/input.txt") as f:
        lines = f.read().splitlines()
    return [list(line) for line in lines]


def select_rolls_to_remove(array_2d: list[list[str]]) -> int:
    rows = len(array_2d)
    cols = len(array_2d[0])

    neighbors = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]

    total = 0

    for i in range(rows):
        for j in range(cols):
            if array_2d[i][j] != "@":
                continue

            adjacent_count = 0
            for di, dj in neighbors:
                ni, nj = i + di, j + dj
                if 0 <= ni < rows and 0 <= nj < cols:
                    if array_2d[ni][nj] in ("@", "X"):
                        adjacent_count += 1

            if adjacent_count < 4:
                array_2d[i][j] = "X"
                total += 1
    return total


def remove_rolls_of_paper(array_2d: list[list[str]]) -> None:
    for i in range(len(array_2d)):
        for j in range(len(array_2d[i])):
            if array_2d[i][j] == "X":
                array_2d[i][j] = "."


def main() -> None:
    array_2d = read_input()

    total_rolls_removed = 0
    rolls_to_remove = 1
    part_1 = None
    while rolls_to_remove > 0:
        rolls_to_remove = select_rolls_to_remove(array_2d)
        remove_rolls_of_paper(array_2d)
        if not part_1:
            part_1 = rolls_to_remove
        total_rolls_removed += rolls_to_remove

    print(f"Part 1: {part_1}")
    print(f"Part 2: {total_rolls_removed}")


if __name__ == "__main__":
    main()
