from collections import namedtuple
from pathlib import Path
from typing import List


def parse_input(path: str) -> List[int]:
    text = Path(path).read_text()
    return text.split("\n")[0].split(","), text.split("\n")[1].split(",")


Cord = namedtuple("Cord", "x y")


def main():
    wire1_instructions, wire2_instructions = parse_input(
        "advent_of_code/2019/advent_of_code_day3/input.txt"
    )
    path1 = create_path(wire1_instructions)
    path2 = create_path(wire2_instructions)

    crossings = set(path1).intersection(set(path2))

    result = min(abs(cord.x) + abs(cord.y) for cord in crossings)
    print(f"Part 1: {result}")
    result = min(path1[crossing] + path2[crossing] for crossing in crossings)
    print(f"Part 2: {result}")


def create_path(instructions):
    DIRECTIONS = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}
    head_x = head_y = head_steps = 0
    path = {}
    for i in instructions:
        direction = i[:1]
        length = int(i[1:])
        dx, dy = DIRECTIONS[direction]
        for _ in range(length):
            head_x += dx
            head_y += dy
            head_steps += 1
            cord = Cord(head_x, head_y)
            path[cord] = head_steps

    return path


if __name__ == "__main__":
    main()
