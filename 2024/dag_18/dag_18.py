from copy import deepcopy

import networkx as nx

GRID_SIZE = 71
NO_OF_BYTES = 1024


def read_input() -> list[tuple[int, int]]:
    """Read the coordinates of incoming byte positions."""
    with open("dag_18/input.txt") as f:
        obstacles = [co.split(",") for co in f.readlines()]
        obstacles = [(int(y), int(x)) for x, y in obstacles]
        return obstacles


class MemorySpaceEscaper:
    """Class for escaping the memory space."""

    def __init__(self, obstacles: list[tuple[int, int]]) -> None:
        self.obstacles = obstacles
        self.start = (0, 0)  # Top Left
        self.exit = (GRID_SIZE - 1, GRID_SIZE - 1)  # Bottom Right

    def initialize_graph(self) -> None:
        """Initialize the graph based on the grid size."""
        self.G = nx.grid_2d_graph(GRID_SIZE, GRID_SIZE)

    def solve_for_no_of_bytes(self, no_of_bytes: int) -> None:
        """Solve the map with a specific number of obstacles (the 'bytes')."""
        self.initialize_graph()

        # Remove obstacles from the grid
        for obstacle in self.obstacles[:no_of_bytes]:
            if obstacle in self.G:
                self.G.remove_node(obstacle)

        shortest_path = nx.shortest_path(self.G, source=self.start, target=self.exit)
        print(f"Minimum number of steps needed to reach the exit: {len(shortest_path) - 1}")

    def find_max_number_of_obstacles(self) -> None:
        """Find the max number of obstacles allowed to fall before the exit is blocked off."""
        print("Finding obstacle which permanently blocks the exit")

        # Make sure the graph is clean
        self.initialize_graph()

        obstacles_to_pop = deepcopy(self.obstacles)
        while obstacles_to_pop:
            obstacle = obstacles_to_pop.pop(0)
            self.G.remove_node(obstacle)
            if nx.has_path(self.G, self.start, self.exit) is False:
                print(f"After adding {obstacle} the exit is blocked")
                break


def main() -> None:
    """Main function for day 16."""
    obstacles = read_input()
    memory_space_escaper = MemorySpaceEscaper(obstacles)
    memory_space_escaper.solve_for_no_of_bytes(NO_OF_BYTES)
    memory_space_escaper.find_max_number_of_obstacles()


if __name__ == "__main__":
    main()
