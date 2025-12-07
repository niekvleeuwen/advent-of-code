def read_input() -> tuple[list, list]:
    """Read input.

    1. Open file
    2. Split the ordering rules and page updates
    3. Split the rules and updates into a list
    """
    with open("dag_5/input.txt") as f:
        ordering_rules, page_updates = f.read().split("\n\n")
        ordering_rules = [page.split("|") for page in ordering_rules.splitlines()]
        page_updates = [page.split(",") for page in page_updates.splitlines()]
        return ordering_rules, page_updates


def is_update_in_order(ordering_rules: list, page_update: list) -> bool:
    """Check if the update follows all rules."""
    for before, after in ordering_rules:
        if before in page_update and after in page_update:
            if page_update.index(before) > page_update.index(after):
                return False
    return True


def order_in_correct_page_update(ordering_rules: list, page_update: list) -> list:
    """Order an incorrectly sorted page update."""
    while not is_update_in_order(ordering_rules, page_update):
        for before, after in ordering_rules:
            if before in page_update and after in page_update:
                before_index = page_update.index(before)
                after_index = page_update.index(after)
                if before_index > after_index:
                    # Swap numbers
                    item = page_update[before_index]
                    del page_update[before_index]
                    page_update.insert(after_index, item)

    return page_update


def middle_page_number(page_update: list) -> int:
    """Retrieve the middel page number."""
    middle_item = page_update[len(page_update) // 2]
    return int(middle_item)


def correctly_ordered_updates(ordering_rules: list, page_update: list) -> int:
    """Sum the middle page number of all correctly ordered updates."""
    if is_update_in_order(ordering_rules, page_update):
        return middle_page_number(page_update)
    return 0


def incorrectly_ordered_updates(ordering_rules: list, page_update: list) -> int:
    """Sum the middle page number of all incorrectly ordered updates, after sorting them."""
    if is_update_in_order(ordering_rules, page_update) is False:
        ordered_page_update = order_in_correct_page_update(ordering_rules, page_update)
        return middle_page_number(ordered_page_update)
    return 0


def main() -> None:
    """Main function for day 5."""
    ordering_rules, page_updates = read_input()

    part_1 = sum([correctly_ordered_updates(ordering_rules, page_update) for page_update in page_updates])
    part_2 = sum([incorrectly_ordered_updates(ordering_rules, page_update) for page_update in page_updates])
    print(f"Result (1): {part_1}")
    print(f"Result (2): {part_2}")


if __name__ == "__main__":
    main()
