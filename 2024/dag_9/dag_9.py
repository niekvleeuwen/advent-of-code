from copy import deepcopy
from typing import TypedDict


class File(TypedDict):
    """Representation of a file."""

    id: str
    starting_index: int
    no_of_blocks: int


def read_input() -> list[str]:
    """Read input.

    1. Open file
    2. Return the disk map
    """
    with open("dag_9/input.txt") as f:
        return list(f.read())


def stretch_disk_map(disk_map: list[str]) -> list[str]:
    """Stretch out the disk map from 12345 to 0..111....22222."""
    current_id = 0
    stretched_disk_map = []
    for i, digit in enumerate(disk_map):
        is_free_space = i % 2 != 0
        for i in range(int(digit)):
            stretched_disk_map.append(str(current_id) if not is_free_space else ".")
        if not is_free_space:
            current_id += 1
    return stretched_disk_map


def compact_disk_map_with_fragmentation(stretched_disk_map: list[str]) -> list[str]:
    """Compact the disk map from 0..111....22222 to 022111222......"""
    while "." in stretched_disk_map:
        for i, digit in enumerate(stretched_disk_map):
            if digit == ".":
                # Retrieve last item that is not free space
                last_item = None
                while last_item is None:
                    last_index = len(stretched_disk_map) - 1
                    last_item = stretched_disk_map[last_index]
                    if last_item == ".":
                        last_item = None
                    del stretched_disk_map[last_index]

                # Insert last item in the free space
                del stretched_disk_map[i]
                stretched_disk_map.insert(i, last_item)

    return stretched_disk_map


def get_first_free_space(stretched_disk_map: list[str], length: int) -> int | None:
    """Return first available space of length in disk map."""
    i = 0
    while i < len(stretched_disk_map):
        digit = stretched_disk_map[i]
        if digit == ".":
            first_index = i
            len_of_free_space = 0
            while digit == "." and i < len(stretched_disk_map) - 1:
                i += 1
                len_of_free_space += 1
                digit = stretched_disk_map[i]
            if len_of_free_space >= length:
                return first_index
        i += 1
    return None


def compact_disk_map_without_fragmentation(stretched_disk_map: list[str]) -> list[str]:
    """Create a map of available spaces in disk map without fragmenting a file."""
    # Calculate a map of blocks
    files = []
    i = len(stretched_disk_map) - 1
    while i > 0:
        no_of_blocks = 0
        starting_index = i
        block_id = stretched_disk_map[i]
        if block_id != ".":
            while stretched_disk_map[i] == block_id:
                starting_index = i
                i -= 1
                no_of_blocks += 1

            file: File = {
                "id": block_id,
                "starting_index": starting_index,
                "no_of_blocks": no_of_blocks,
            }
            files.append(file)
        else:
            i -= 1

    for file in files:
        # Find first available free index
        first_free_index = get_first_free_space(stretched_disk_map, file["no_of_blocks"])

        if first_free_index and first_free_index < file["starting_index"]:
            # Remove file from original location
            for i in range(file["starting_index"] + file["no_of_blocks"], file["starting_index"], -1):
                del stretched_disk_map[i - 1]
                stretched_disk_map.insert(i - 1, ".")

            # Add file to new location
            for i in range(first_free_index, first_free_index + file["no_of_blocks"]):
                stretched_disk_map[i] = file["id"]

    return stretched_disk_map


def calculate_checksum(disk_map: list[str]) -> int:
    """Checksum calculation.

    To calculate the checksum, add up the result of multiplying each of these blocks'
    position with the file ID number it contains.
    """
    disk_map_formatted = [0 if val == "." else int(val) for val in disk_map]
    return sum([i * v for i, v in enumerate(disk_map_formatted)])


def main() -> None:
    """Main function for day 9."""
    disk_map = read_input()

    stretched_disk_map = stretch_disk_map(disk_map)

    compacted_disk_map_1 = compact_disk_map_with_fragmentation(deepcopy(stretched_disk_map))
    print(f"Checksum (1): {calculate_checksum(compacted_disk_map_1)}")

    compacted_disk_map_2 = compact_disk_map_without_fragmentation(deepcopy(stretched_disk_map))
    print(f"Checksum (2): {calculate_checksum(compacted_disk_map_2)}")


if __name__ == "__main__":
    main()
