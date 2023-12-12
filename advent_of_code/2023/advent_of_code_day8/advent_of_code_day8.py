from pathlib import Path
from typing import List
import math
from itertools import cycle


def parse_input(path: str) -> List[int]:
    return Path(path).read_text().split("\n")


def run(start, end, map, instructions):
    location = start
    for steps, instruction in enumerate(instructions, start=1):
        location = map[location][0 if instruction == "L" else 1]
        if location.endswith("Z") or location == end:
            return steps


def main():
    puzzle_input = parse_input("advent_of_code/2023/advent_of_code_day8/input.txt")
    # puzzle_input = parse_input("advent_of_code/2023/advent_of_code_day8/input_small.txt")
    instructions = cycle(puzzle_input[0])

    map = {
        line.split(" = ")[0]: (
            line.split(" = ")[1].split(", ")[0][1:],
            line.split(" = ")[1].split(", ")[1][:-1],
        )
        for line in puzzle_input[2:]
    }
    
    print(f"Part 1: {run('AAA','ZZZ', map, instructions)}")

    starts = [pos for pos in map if pos.endswith("A")]
    result = math.lcm(*[run(start, start, map, instructions) for start in starts])

    print(f"Part 2: {result}")


if __name__ == "__main__":
    main()
