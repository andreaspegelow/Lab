from pathlib import Path
import math


def parse_input(path: str):
    return Path(path).read_text().split("\n")


def get_sounding_heights(x: int, y: int, floor_map: list):
    try:
        right = int(floor_map[y][x + 1])
    except IndexError:
        right = 9
    try:
        left = int(floor_map[y][x - 1]) if 0 <= x - 1 else 9
    except IndexError:
        left = 9
    try:
        up = int(floor_map[y - 1][x]) if 0 <= y - 1 else 9
    except IndexError:
        up = 9
    try:
        down = int(floor_map[y + 1][x])
    except IndexError:
        down = 9
    return int(right), int(left), int(up), int(down)


def find_basin(x: int, y: int, floor_map: list, included_positions):

    included_positions.add((x, y))
    right, left, up, down = get_sounding_heights(x, y, floor_map)

    if right != 9 and (x + 1, y) not in included_positions:
        included_positions.union(find_basin(x + 1, y, floor_map, included_positions))
    if left != 9 and (x - 1, y) not in included_positions:
        included_positions.union(find_basin(x - 1, y, floor_map, included_positions))
    if up != 9 and (x, y - 1) not in included_positions:
        included_positions.union(find_basin(x, y - 1, floor_map, included_positions))
    if down != 9 and (x, y + 1) not in included_positions:
        included_positions.union(find_basin(x, y + 1, floor_map, included_positions))
    return included_positions


def main():
    floor_map = parse_input("advent_of_code/2021/advent_of_code_day9/input.txt")
    total_risk = 0
    basins = []
    basin_sizes = []
    for y in range(len(floor_map)):
        for x in range(len(floor_map[0])):
            right, left, up, down = get_sounding_heights(x, y, floor_map)
            current_pos_height = int(floor_map[y][x])
            if (
                current_pos_height < right
                and current_pos_height < left
                and current_pos_height < up
                and current_pos_height < down
            ):
                total_risk += current_pos_height + 1
                basin = find_basin(x, y, floor_map, set())
                basin_sizes.append(len(basin))
                basins.append(basin)

    print(f"Part 1: {total_risk}")

    basin_sizes.sort()
    print(f"Part 2: {math.prod(basin_sizes[-3:])}")

    symbols = "#?*.-&%|<>!'"
    for i, basin in enumerate(basins):
        for x, y in basin:
            floor_map[y] = (
                floor_map[y][:x] + symbols[i % len(symbols)] + floor_map[y][x + 1 :]
            )
    with open("advent_of_code/2021/advent_of_code_day9/output.txt", "w") as out_file:
        for row in floor_map:
            out_file.write(row.replace("9", " ") + "\n")


if __name__ == "__main__":
    main()
