from pathlib import Path
from typing import List


def parse_input(path: str) -> List[int]:
    return [list(map(int, line.split())) for line in Path(path).read_text().split("\n")]


def extrapolate(readings):
    diff = [b - a for a, b in zip(readings, readings[1:])]
    return readings[-1] + extrapolate(diff) if len(readings) != 0 else 0


def main():
    puzzle_input = parse_input("advent_of_code/2023/advent_of_code_day9/input.txt")
    result = sum(map(extrapolate, puzzle_input))
    print(f"Part 1: {result}")

    result = sum(extrapolate(line[::-1]) for line in puzzle_input)
    print(f"Part 2: {result}")


if __name__ == "__main__":
    main()
