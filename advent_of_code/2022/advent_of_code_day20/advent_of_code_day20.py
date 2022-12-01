from pathlib import Path
from typing import List


def parse_input(path: str) -> List[int]:
    return [int(i) for i in Path(path).read_text().split("\n")]


def main():
    puzzle_input = parse_input("advent_of_code/2022/advent_of_code_day20/input.txt")


if __name__ == "__main__":
    main()
