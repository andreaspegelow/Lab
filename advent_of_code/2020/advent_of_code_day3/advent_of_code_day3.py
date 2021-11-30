from dataclasses import dataclass
from enum import Enum
from functools import partial, reduce


@dataclass
class Slope:
    right: int
    down: int


class Map_object(Enum):
    TREE = "#"
    OPEN = "."


def parse_input(path: str) -> list:
    with open(path) as f:
        lines = [line.rstrip() for line in f.readlines()]
    return lines


def count_trees_hit(slope: Slope, mountain: list):
    wrap_around_width = len(mountain[0])
    number_of_trees = 0

    for step in range(len(mountain)):
        row = slope.down * step
        colum = (slope.right * step) % wrap_around_width

        if row > len(mountain):
            break

        if mountain[row][colum] == Map_object.TREE.value:
            number_of_trees += 1

    return number_of_trees


def main():

    mountain = parse_input("advent_of_code/2020/advent_of_code_day3/input.txt")

    # Part 1
    slope = Slope(right=3, down=1)
    number_of_trees = count_trees_hit(slope, mountain)
    print(f"Part 1: Number of trees hit: {number_of_trees}")

    # Part 2
    slopes = [
        Slope(right=1, down=1),
        Slope(right=3, down=1),
        Slope(right=5, down=1),
        Slope(right=7, down=1),
        Slope(right=1, down=2),
    ]
    result = map(partial(count_trees_hit, mountain=mountain), slopes)
    result = reduce(lambda x, y: x * y, result)
    print(f"Part 2: {result}")


if __name__ == "__main__":
    main()
