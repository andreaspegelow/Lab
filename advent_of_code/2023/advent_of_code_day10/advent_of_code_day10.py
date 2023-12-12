from pathlib import Path
from typing import List
from dataclasses import dataclass
from itertools import cycle


@dataclass
class PipeInfo:
    input_dir: list
    output_dir: list

directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
pipes = {
    "|": PipeInfo([directions[1], directions[3]], [directions[1], directions[3]]),
    "-": PipeInfo([directions[0], directions[2]], [directions[0], directions[2]]),
    "L": PipeInfo([directions[1], directions[2]], [directions[0], directions[3]]),
    "J": PipeInfo([directions[1], directions[0]], [directions[2], directions[3]]),
    "7": PipeInfo([directions[0], directions[3]], [directions[2], directions[1]]),
    "F": PipeInfo([directions[2], directions[3]], [directions[0], directions[1]]),
}


def parse_input(path: str) -> List[int]:
    return Path(path).read_text().split("\n")


def main():
    puzzle_input = parse_input(
        "advent_of_code/2023/advent_of_code_day10/input.txt"
    )
    start_point = None
    for y, line in enumerate(puzzle_input):
        for x, tile in enumerate(line):
            if tile == "S":
                start_point = (x, y)

    current_location = start_point
    oldLocation = None
    path = [start_point]
    for dir in cycle(directions):
        if current_location != start_point and dir not in pipes[puzzle_input[current_location[1]][current_location[0]]].output_dir:
            continue

        next_location = (
            current_location[0] + dir[0],
            current_location[1] + dir[1],
        )
        next_pipe = puzzle_input[next_location[1]][next_location[0]]

        if next_pipe == "S" and next_location != oldLocation:
            break

        if (
            next_pipe
            in [pipe for pipe, pipe_info in pipes.items() if dir in pipe_info.input_dir]
            and next_location != oldLocation
        ):
            oldLocation = current_location
            current_location = next_location
            path.append(current_location)
    print(f"Part 1: {len(path)//2}")


if __name__ == "__main__":
    main()
