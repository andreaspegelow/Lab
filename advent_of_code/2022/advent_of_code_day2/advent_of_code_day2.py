from pathlib import Path
from typing import List

part1_mapping = {"X": "A", "Y": "B", "Z": "C"}
shape_points = {"A": 1, "B": 2, "C": 3}
rules = ["A", "C", "B"]


def parse_input(path: str) -> List[int]:
    return [game.split(" ") for game in Path(path).read_text().split("\n")]


def round_score(op, me):
    if op == me:
        return 3
    return 0 if rules[(rules.index(op) + 1) % 3] == me else 6


def select_shape(op, outcome):
    if outcome == "X":
        return rules[(rules.index(op) + 1) % 3]
    if outcome == "Y":
        return op
    if outcome == "Z":
        return rules[(rules.index(op) - 1) % 3]


def main():
    puzzle_input = parse_input("advent_of_code/2022/advent_of_code_day2/input.txt")
    total_score = sum(
        shape_points[part1_mapping[me]] + round_score(op, part1_mapping[me])
        for op, me in puzzle_input
    )
    print(f"Part 1: {total_score}")

    total_score = sum(
        shape_points[select_shape(op, outcome)] + round_score(op, select_shape(op, outcome))
        for op, outcome in puzzle_input
    )
    print(f"Part 2: {total_score}")


if __name__ == "__main__":
    main()
