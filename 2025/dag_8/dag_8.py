import math
from pathlib import Path

import click
import networkx as nx
import numpy as np


def read_input(file_path: Path) -> list:
    """Read input."""
    with open(file_path) as f:
        vectors = []
        for line in f.read().splitlines():
            vectors.append(tuple(int(c) for c in line.split(",")))
        return vectors


def k_closest_pairs(vectors: list[tuple], k: int = None) -> list[tuple]:
    """Compute the k closest vector pairs.

    Uses exact Euclidean distance. All pairwise distances are computed once,
    then the k smallest distinct pairs (i < j) are selected and returned
    in ascending order of distance.
    """
    X = np.asarray(vectors, dtype=np.float32)
    n = X.shape[0]
    if n < 2:
        return []

    s = np.sum(X * X, axis=1)
    D2 = s[:, None] + s[None, :] - 2.0 * (X @ X.T)

    iu, ju = np.triu_indices(n, k=1)
    d2 = D2[iu, ju]

    if k is None:
        order = np.argsort(d2)
    else:
        k = min(k, d2.size)
        sel = np.argpartition(d2, k - 1)[:k]
        order = sel[np.argsort(d2[sel])]

    out = []
    for idx in order:
        i, j = int(iu[idx]), int(ju[idx])
        out.append((tuple(vectors[i]), tuple(vectors[j])))

    return out


def part_1(puzzle_input: list, no_of_iterations: int = 10) -> int:
    graph = nx.Graph()
    graph.add_nodes_from(puzzle_input)

    for pair in k_closest_pairs(puzzle_input, k=no_of_iterations):
        graph.add_edge(*pair)

    # Get the largest 3 results and multiply
    result = [len(v) for v in sorted(nx.connected_components(graph), key=len, reverse=True)]
    return math.prod(result[:3])


def part_2(puzzle_input: list) -> int:
    graph = nx.Graph()
    graph.add_nodes_from(puzzle_input)

    pairs = k_closest_pairs(puzzle_input)

    last_connected_pair = None
    for pair in pairs:
        if nx.number_connected_components(graph) == 1:
            break

        graph.add_edge(*pair)
        last_connected_pair = pair

    return last_connected_pair[0][0] * last_connected_pair[1][0]


@click.command()
# test flag
@click.option("--test", is_flag=True, help="Run with test input")
def cli(test: bool) -> None:
    """CLI function."""
    file_path = Path(__file__).parent / ("example.txt" if test else "input.txt")
    puzzle_input = read_input(file_path)
    print(f"Part 1: {part_1(puzzle_input, no_of_iterations=1000 if not test else 10)}")
    print(f"Part 2: {part_2(puzzle_input)}")


if __name__ == "__main__":
    cli()
