DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def read_input() -> list[list[int]]:
    """Read input.

    1. Open file
    2. Return the topographic map
    """
    with open("dag_10/input.txt") as f:
        lines = [line for line in f.read().splitlines()]

        map = []
        for line in lines:
            map.append([int(c) for c in line])
        return map


def trace_routes_part_1(topographic_map: list[list[int]], start_x: int, start_y: int) -> int:
    """Trace routes from a given starting position and count the number of reachable tops."""
    rows, cols = len(topographic_map), len(topographic_map[0])
    coordinates_to_visit = [(start_x, start_y)]
    no_of_trailheads = 0

    while coordinates_to_visit:
        current_x, current_y = coordinates_to_visit.pop(0)

        if topographic_map[current_x][current_y] == 9:
            no_of_trailheads += 1

        for dx, dy in DIRECTIONS:
            new_x, new_y = current_x + dx, current_y + dy
            if 0 <= new_x < rows and 0 <= new_y < cols and (new_x, new_y) not in coordinates_to_visit:
                if topographic_map[new_x][new_y] == topographic_map[current_x][current_y] + 1:
                    coordinates_to_visit.append((new_x, new_y))

    return no_of_trailheads


def trace_routes_part_2(topographic_map: list[list[int]], x: int, y: int) -> int:
    """Trace routes from a given starting position and count the number of valid paths."""
    if topographic_map[x][y] == 9:
        return 1

    rows, cols = len(topographic_map), len(topographic_map[0])
    trail_count = 0

    for dx, dy in DIRECTIONS:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < rows and 0 <= new_y < cols:
            if topographic_map[new_x][new_y] == topographic_map[x][y] + 1:
                trail_count += trace_routes_part_2(topographic_map, new_x, new_y)

    return trail_count


def main() -> None:
    """Main function for day 10."""
    topographic_map = read_input()

    rows, cols = len(topographic_map), len(topographic_map[0])

    score_part_1 = 0
    score_part_2 = 0
    for i in range(rows):
        for j in range(cols):
            if topographic_map[i][j] == 0:
                score_part_1 += trace_routes_part_1(topographic_map, i, j)
                score_part_2 += trace_routes_part_2(topographic_map, i, j)

    print("Total Score (1):", score_part_1)
    print("Total Score (2):", score_part_2)


if __name__ == "__main__":
    main()
