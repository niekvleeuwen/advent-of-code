def read_input() -> tuple[list[tuple[int, int]], list[int]]:
    with open("2025/dag_5/input.txt") as f:
        lines = f.read().splitlines()
    sep = lines.index("")

    ingredient_ids = [int(v) for v in lines[sep + 1 :]]

    id_ranges = []
    for r in lines[:sep]:
        s, e = r.split("-")
        id_ranges.append((int(s), int(e)))

    return id_ranges, ingredient_ids


def part_1(id_ranges: list[tuple[int, int]], ingredient_ids: list[int]) -> int:
    fresh_ingredients = 0
    for ingredient in ingredient_ids:
        for r in id_ranges:
            if r[0] <= ingredient <= r[1]:
                fresh_ingredients += 1
                break
    return fresh_ingredients


def part_2(id_ranges: list[tuple[int, int]]) -> int:
    # Sort id ranges
    id_ranges = sorted(id_ranges, key=lambda x: x[0])

    # Merge overlapping ranges
    merged = []
    for start, end in id_ranges:
        # directly append first result
        if not merged:
            merged.append([start, end])
            continue

        # Set end of last item
        end_of_last_item = merged[-1][1]
        if start <= end_of_last_item:
            merged[-1][1] = max(end_of_last_item, end)
        else:
            merged.append([start, end])

    total_fresh = sum(end - start + 1 for start, end in merged)
    return total_fresh


def main() -> None:
    id_ranges, ingredient_ids = read_input()
    print(f"Part 1: {part_1(id_ranges, ingredient_ids)}")
    print(f"Part 2: {part_2(id_ranges)}")


if __name__ == "__main__":
    main()
