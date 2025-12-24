from functools import lru_cache
from pathlib import Path

import click
import networkx as nx


def read_input(file_path: Path) -> list[list[str]]:
    """Read input."""
    with open(file_path) as f:
        connected_devices = {}
        for line in f.read().splitlines():
            node, edges = line.split(": ")
            connected_devices[node] = edges.split(" ")
        return connected_devices


def build_graph(connected_devices: dict[str, list[str]]) -> nx.Graph:
    G = nx.DiGraph()

    for u, vs in connected_devices.items():
        for v in vs:
            G.add_edge(u, v)

    if not nx.is_directed_acyclic_graph(G):
        raise ValueError("Graph is not a DAG.")

    return G


def count_paths_between_nodes(G: nx.DiGraph, start: str, end: str) -> int:
    @lru_cache(maxsize=None)
    def count_paths_from(node: str) -> int:
        if node == end:
            return 1
        return sum(count_paths_from(v) for v in G.successors(node))

    return count_paths_from(start)


def count_paths_via_nodes(G: nx.DiGraph, start: str, end: str, via_nodes: list[str]) -> int:
    nodes = [start] + list(via_nodes) + [end]
    total = 1
    for a, b in zip(nodes, nodes[1:]):
        total *= count_paths_between_nodes(G, a, b)
    return total


@click.command()
# test flag
@click.option("--test", is_flag=True, help="Run with test input")
def cli(test: bool) -> None:
    """CLI function."""
    file_path = Path(__file__).parent / ("example.txt" if test else "input.txt")
    puzzle_input = read_input(file_path)
    G = build_graph(puzzle_input)
    print(f"Part 1: {count_paths_between_nodes(G, "you", "out")}")
    print(f"Part 2: {count_paths_via_nodes(G, "svr", "out", ["fft", "dac"])}")


if __name__ == "__main__":
    cli()
