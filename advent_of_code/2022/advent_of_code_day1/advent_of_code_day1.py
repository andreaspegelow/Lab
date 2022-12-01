from pathlib import Path
from typing import List


def parse_input(path: str) -> List[int]:
    return Path(path).read_text().split("\n\n")


def main():
    elfs = parse_input("advent_of_code/2022/advent_of_code_day1/input.txt")

    biggest_load = max(sum(map(int, elf.split("\n"))) for elf in elfs)
    print(f"Part 1: {biggest_load}")

    top3_total = sum(sorted(sum(map(int, elf.split("\n"))) for elf in elfs)[-3:])
    print(f"Part 2: {top3_total}")


if __name__ == "__main__":
    main()
