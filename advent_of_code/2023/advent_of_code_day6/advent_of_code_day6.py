from pathlib import Path
from typing import List
import math


def parse_input(path: str) -> List[int]:
    return Path(path).read_text().split("\n")


def game_simulator(hold_time, game_time):
    return (game_time - hold_time) * hold_time


def main():
    puzzle_input = parse_input("advent_of_code/2023/advent_of_code_day6/input.txt")
    times = list(map(int, puzzle_input[0].split(":")[1].split()))
    distance = list(map(int, puzzle_input[1].split(":")[1].split()))
    games = list(zip(times, distance))

    count = 1
    for game_time, record in games:
        count *= sum([1 for hold_time in range(1, game_time)if game_simulator(hold_time, game_time) > record])

    print(f"Part 1: {count}")

    game_time = int(puzzle_input[0].split(":")[1].replace(" ", ""))
    record = int(puzzle_input[1].split(":")[1].replace(" ", ""))

    a = -1
    b = game_time
    c = -record

    d = (b**2) - (4*a*c)

    t1 = (-b-math.sqrt(d))/(2*a)
    t2 = (-b+math.sqrt(d))/(2*a)

    print(f"Part 2: {int(round(t1-t2, 0))}")


if __name__ == "__main__":
    main()
