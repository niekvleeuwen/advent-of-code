DIRECTIONS = {"^": (-1, 0), "v": (1, 0), ">": (0, 1), "<": (0, -1)}


def read_input(part_2: bool = False) -> tuple[list[list[str]], list[str]]:
    """Read input.

    1. Open file
    2. Return a tuple with the grid and instructions
    """
    with open("dag_15/input.txt") as f:
        grid, instructions = f.read().split("\n\n")
        if part_2:
            grid = grid.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")
        grid = [list(s) for s in grid.splitlines()]
        instructions = list(instructions.replace("\n", ""))
        return grid, instructions


def locate_robot(grid: list[list[str]]) -> tuple[int, int]:
    """Finds the robot's initial position in the grid."""
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell == "@":
                return row_idx, col_idx
    raise ValueError("No robot found in grid!")


def check_move_effect(
    grid: list[list[str]], start_x: int, start_y: int, dx: int, dy: int
) -> list[tuple[int, int]] | None:
    """Collects all cells affected by the robot's move based on the direction."""
    queue = [(start_x, start_y)]
    visited = set(queue)

    for x, y in queue:
        next_x, next_y = x + dx, y + dy
        if grid[next_x][next_y] in "O[]":
            if (next_x, next_y) not in visited:
                queue.append((next_x, next_y))
                visited.add((next_x, next_y))

            if grid[next_x][next_y] == "[" and (next_x, next_y + 1) not in visited:
                queue.append((next_x, next_y + 1))
                visited.add((next_x, next_y + 1))

            if grid[next_x][next_y] == "]" and (next_x, next_y - 1) not in visited:
                queue.append((next_x, next_y - 1))
                visited.add((next_x, next_y - 1))
        elif grid[next_x][next_y] == "#":
            return None

    return queue


def apply_move(grid: list[list[str]], targets: list[tuple[int, int]], dx: int, dy: int) -> list[list[str]]:
    """Applies the robot's move to the grid and returns the updated grid."""
    rows, cols = len(grid), len(grid[0])
    new_grid = [[grid[row][col] for col in range(cols)] for row in range(rows)]

    for x, y in targets:
        new_grid[x][y] = "."
    for x, y in targets:
        new_grid[x + dx][y + dy] = grid[x][y]

    return new_grid


def calculate_score(grid: list[list[str]]) -> int:
    """Calculates the score based on the final grid state."""
    score = 0
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell in "[O":
                score += 100 * row_idx + col_idx
    return score


def solve(grid: list[list[str]], instructions: list[str]) -> int:
    """Executes all instructions on the given grid.."""
    current_x, current_y = locate_robot(grid)

    for instruction in instructions:
        dx, dy = DIRECTIONS[instruction]

        if move := check_move_effect(grid, current_x, current_y, dx, dy):
            grid = apply_move(grid, move, dx, dy)
            current_x += dx
            current_y += dy

    return calculate_score(grid)


def main() -> None:
    """Main function for day 15."""
    grid, instructions = read_input()
    print("Answer (1):", solve(grid, instructions))
    grid, instructions = read_input(part_2=True)
    print("Answer (2):", solve(grid, instructions))


if __name__ == "__main__":
    main()
