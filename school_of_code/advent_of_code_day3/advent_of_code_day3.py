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
        lines = f.readlines()
        lines = [line.rstrip() for line in lines]
    return lines


def count_trees(slope: Slope, mountain: list):
    wrap_around_width = len(mountain[0])
    number_of_trees = 0

    for i in range(len(mountain)):
        y = slope.down * i
        x = (slope.right * i) % wrap_around_width

        if y > len(mountain):
            break

        if mountain[y][x] == Map_object.TREE.value:
            number_of_trees += 1

    return number_of_trees


def main():

    mountain = parse_input("school_of_code/advent_of_code_day3/input.txt")

    # Part 1
    slope = Slope(right=3, down=1)
    number_of_trees = count_trees(slope, mountain)
    print(f"Part 1: Number of trees hit: {number_of_trees}")

    # Part 2
    slopes = [
        Slope(right=1, down=1),
        Slope(right=3, down=1),
        Slope(right=5, down=1),
        Slope(right=7, down=1),
        Slope(right=1, down=2),
    ]
    result = map(partial(count_trees, mountain=mountain), slopes)
    result = reduce(lambda x, y: x * y, result)
    print(f"Part 2: {result}")


if __name__ == "__main__":
    main()
