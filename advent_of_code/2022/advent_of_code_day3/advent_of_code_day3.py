import string
from pathlib import Path
from typing import List


def parse_input(path: str) -> List[int]:
    return Path(path).read_text().split("\n")


def main():
    rugsacks = parse_input("advent_of_code/2022/advent_of_code_day3/input.txt")
    alphabet = string.ascii_lowercase + string.ascii_uppercase

    count = 0
    for rugsack in rugsacks:
        half = len(rugsack) // 2
        common = {item for item in rugsack[:half] if item in rugsack[half:]}.pop()
        count += alphabet.index(common) + 1
    print(f"Part 1: {count}")

    count = 0
    for i, rugsack in enumerate(rugsacks[::3]):
        i *= 3
        badge = {
            item
            for item in rugsack
            if item in rugsacks[i + 1] and item in rugsacks[i + 2]
        }.pop()
        count += alphabet.index(badge) + 1
    print(f"Part 2: {count}")


if __name__ == "__main__":
    main()
