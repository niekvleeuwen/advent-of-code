import networkx as nx

DIRECTIONS = (1, -1, 1j, -1j)


def read_input(filename: str = "dag_16/input.txt") -> list[list[str]]:
    """Read the maze input from a file."""
    with open(filename) as f:
        return [list(line.strip()) for line in f]


def build_graph(maze: list[list[str]]) -> tuple[nx.DiGraph, tuple[complex, complex]]:  # noqa: C901
    """Builds a directed graph representation of the maze.

    Args:
        maze: A 2D list representation of the maze.

    Returns:
        The graph and starting node.

    """
    graph = nx.DiGraph()
    start, end = None, None

    rows, cols = len(maze), len(maze[0])

    for i in range(rows):
        for j in range(cols):
            char = maze[i][j]
            if char == "#":
                continue

            # Map grid coordinates to complex numbers for easier traversal
            z = i + 1j * j
            if char == "S":
                start = (z, 1j)  # Start node with initial direction
            elif char == "E":
                end = z

            # Add all valid movement nodes
            for dz in DIRECTIONS:
                graph.add_node((z, dz))

    if not start:
        raise ValueError("No start (S) found.")

    # Create edges for movements and rotations
    for z, dz in graph.nodes:
        if (z + dz, dz) in graph.nodes:  # Forward movement
            graph.add_edge((z, dz), (z + dz, dz), weight=1)
        for rot in (-1j, 1j):  # Rotation to change direction
            graph.add_edge((z, dz), (z, dz * rot), weight=1000)

    # Connect the end node to a special "end" node
    for dz in DIRECTIONS:
        graph.add_edge((end, dz), "end", weight=0)

    return graph, start


def find_part_2_result(graph: nx.DiGraph, start: tuple[complex, complex]) -> int:
    """Calculates the number of unique nodes visited in all shortest paths to the end.

    Args:
        graph: The directed graph representation of the maze.
        start: The starting node.

    Returns:
        The count of unique nodes in all shortest paths.

    """
    paths = nx.all_shortest_paths(graph, start, "end", weight="weight")
    unique_nodes = {z for path in paths for z, _ in path[:-1]}  # Exclude the "end" node
    return len(unique_nodes)


def solve(maze: list[list[str]]) -> None:
    """Solves the maze and prints the results for both parts.

    Args:
        maze: A 2D list representation of the maze.

    """
    graph, start = build_graph(maze)

    part_1 = nx.shortest_path_length(graph, start, "end", weight="weight")
    part_2 = find_part_2_result(graph, start)

    print(f"Result (1): {part_1}")
    print(f"Result (2): {part_2}")


def main() -> None:
    """Main function for day 16."""
    maze = read_input()
    solve(maze)


if __name__ == "__main__":
    main()
