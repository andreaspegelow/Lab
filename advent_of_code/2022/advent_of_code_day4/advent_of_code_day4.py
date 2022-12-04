from pathlib import Path
from typing import List


def parse_input(path: str) -> List[int]:
    p = []
    for pairs in Path(path).read_text().split("\n"):
        l = []
        for section in pairs.split(","):
            start, end = map(int, section.split("-"))
            l.append(range(start, end))
        l = sorted(l, key=lambda k: k.start)
        p.append(l)
    return p


def main():
    pairs = parse_input("advent_of_code/2022/advent_of_code_day4/input.txt")
    selected = [
        (first, second)
        for first, second in pairs
        if set(first).issubset(set(second)) or set(second).issubset(set(first))
    ]
    print(f"Part 1: {len(selected)}")

    selected = [
        (first, second) for first, second in pairs if first.stop >= second.start
    ]
    print(f"Part 2: {len(selected)}")


if __name__ == "__main__":
    main()
