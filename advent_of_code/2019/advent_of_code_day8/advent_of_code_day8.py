from pathlib import Path
from typing import List


def parse_input(path: str) -> List[int]:
    return [int(i) for i in Path(path).read_text().split("\n")]


def main():
    input = parse_input("advent_of_code/2019/advent_of_code_day8/input.txt")


if __name__ == "__main__":
    main()
