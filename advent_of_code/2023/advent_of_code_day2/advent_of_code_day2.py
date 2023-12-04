from pathlib import Path
from typing import List
import re
import math

show_pattern = r"([0-9]+) (red|blue|green)"
game_pattern = r"Game ([0-9]+)"

max_colurs = {"blue": 14, "red": 12, "green": 13}


def parse_input(path: str) -> List[int]:
    return Path(path).read_text().split("\n")


def main():
    puzzle_input = parse_input("advent_of_code/2023/advent_of_code_day2/input.txt")
    
    count = 0
    for game in puzzle_input:
        for shows in re.findall(show_pattern, game):
            if int(shows[0]) > max_colurs[shows[1]]:
                break
        else:
            count += int(re.match(game_pattern, game).group(1))
    print(f"Part 1: {count}")

    count = 0
    for game in puzzle_input:
        needed = {"blue": 0, "red": 0, "green": 0}
        for shows in re.findall(show_pattern, game):
            if needed[shows[1]] < int(shows[0]):
                needed[shows[1]] = int(shows[0])
        count += math.prod(needed.values())
    print(f"Part 2: {count}")


if __name__ == "__main__":
    main()
