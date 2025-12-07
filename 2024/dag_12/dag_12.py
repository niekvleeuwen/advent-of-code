from collections import defaultdict

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def read_input() -> list[list[str]]:
    """Read input.

    1. Open file
    2. Return the garden map
    """
    with open("dag_12/input.txt") as f:
        return [list(line) for line in f.read().splitlines()]


class GardenCalculator:
    """Calculates the cost of a perimeter."""

    def __init__(self, garden_map: list[list[str]]) -> None:
        self.garden_map = garden_map
        self.rows, self.cols = len(garden_map), len(garden_map[0])
        self.visited = []
        self.nodes = defaultdict(set)

    def execute(self) -> tuple[int, int]:
        """Execute the GardenCalculator to calculate prices for both part 1 and part 2."""
        visited = set()

        total_price_1 = 0
        total_price_2 = 0
        for y in range(self.rows):
            for x in range(self.cols):
                if (x, y) not in visited:
                    plant_type = self.garden_map[x][y]
                    nodes = self.calculate_nodes_for_plant_type(x, y, plant_type, visited)
                    area = len(nodes)
                    perimeter = self.calculate_perimeter(nodes)
                    sides = self.calculate_sides(perimeter)
                    total_price_1 += area * len(perimeter)
                    total_price_2 += area * len(sides)

        return total_price_1, total_price_2

    def calculate_nodes_for_plant_type(self, start_x: int, start_y: int, plant_type: str, visited: set) -> set:
        """Starting from a given point, find all nodes for the same plant type."""
        coordinates_to_visit = [(start_x, start_y)]
        nodes_in_area = set(coordinates_to_visit)

        while coordinates_to_visit:
            x, y = coordinates_to_visit.pop()

            # Skip coordinate if it is part of another area or in the current area
            if (x, y) in visited:
                continue

            visited.add((x, y))

            nodes_in_area.add((x, y))

            # Check for same plant types in all directions
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy

                if self.coordinate_is_valid(nx, ny) and self.garden_map[nx][ny] == plant_type:
                    coordinates_to_visit.append((nx, ny))

        return nodes_in_area

    def calculate_perimeter(self, nodes: set) -> set:
        """Calculate the perimeter for the given nodes."""
        perimeter = []
        for x, y in nodes:
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                if self.coordinate_is_valid(nx, ny) is False or (nx, ny) not in nodes:
                    perimeter.append(((x, y), (nx, ny)))
        return set(perimeter)

    def calculate_sides(self, perimeter: set) -> set:
        """Calculate the number of sides given the perimeter of the nodes."""
        sides = set()
        for node_1, node_2 in perimeter:
            for dx, dy in [(0, 1), (1, 0)]:
                n1x, n1y = node_1
                n2x, n2y = node_2
                # If translated perimeter is in existing perimeter, don't add a side
                if ((n1x + dx, n1y + dy), (n2x + dx, n2y + dy)) in perimeter:
                    break
            else:
                sides.add((node_1, node_2))

        return sides

    def coordinate_is_valid(self, x: int, y: int) -> bool:
        """Check if a coordinate is valid."""
        return x >= 0 and y >= 0 and x < self.rows and y < self.cols


def main() -> None:
    """Main function for day 12."""
    garden_map = read_input()

    total_price_1, total_price_2 = GardenCalculator(garden_map).execute()
    print(f"Total price (1): {total_price_1}")
    print(f"Total price (2): {total_price_2}")


if __name__ == "__main__":
    main()
