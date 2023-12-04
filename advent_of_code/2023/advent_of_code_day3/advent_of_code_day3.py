from pathlib import Path
from typing import List
import re
import collections

pattern = r"([0-9]+)"


def parse_input(path: str) -> List[int]:
    return Path(path).read_text().split("\n")


def contains_symbol(string, symbol):
    if symbol:
        return symbol if symbol in string else None

    return x if bool(x := re.sub("\.", "", string)) else None


def surrounded_by_symbol(start, end, row, line, puzzle_input, symbol=None, skipp=None):
    start_offset = -1 if start != 0 else 0
    end_offset = 1 if end != len(line) else 0

    if start != 0 and contains_symbol(line[start - 1], symbol):
        return start - 1, row

    if end != len(line) and contains_symbol(line[end], symbol):
        return end, row

    # Over
    if row != 0 and (
        symbol := contains_symbol(
            puzzle_input[row - 1][start + start_offset : end + end_offset], symbol
        )
    ):
        return (
            start
            + start_offset
            + puzzle_input[row - 1][start + start_offset : end + end_offset].index(
                symbol
            ),
            row - 1,
        )

    # Under
    if row != len(puzzle_input) - 1 and (
        symbol := contains_symbol(
            puzzle_input[row + 1][start + start_offset : end + end_offset], symbol
        )
    ):
        return (
            start
            + start_offset
            + puzzle_input[row + 1][start + start_offset : end + end_offset].index(
                symbol
            ),
            row + 1,
        )
    return False


def main():
    puzzle_input = parse_input("advent_of_code/2023/advent_of_code_day3/input.txt")

    count = 0
    for row, line in enumerate(puzzle_input):
        for m in re.finditer(pattern, line):
            p = m.group(0)
            start = m.start()
            end = m.end()

            if surrounded_by_symbol(start, end, row, line, puzzle_input):
                count += int(p)

    print(f"Part 1 : {count}")

    possible_gears = collections.defaultdict(list)
    for row, line in enumerate(puzzle_input):
        for m in re.finditer(pattern, line):
            p = m.group(0)
            start = m.start()
            end = m.end()

            if result := surrounded_by_symbol(start, end, row, line, puzzle_input, "*"):
                possible_gears[(result[0], result[1])].append(int(p))

    count = sum(
        [value[0] * value[1] for value in possible_gears.values() if len(value) == 2]
    )

    print(f"Part 2 : {count}")


if __name__ == "__main__":
    main()
