from pathlib import Path
import cProfile

DIRECTIONS = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]

OCCUPIED_SEAT = "#"
EMPTY_SEAT = "L"
FLOOR = "."


def parse_input(path: str):
    return [list(row) for row in Path(path).read_text().splitlines()]


def count_occupied_seats(map):
    return sum([row.count(OCCUPIED_SEAT) for row in map])


def is_all_surrounding_free(start_x, start_y, map, x_limit, y_limit, max_steps):
    for direction in DIRECTIONS:
        step = 0
        x, y = start_x, start_y
        dx, dy = direction
        while not max_steps or step < max_steps:
            step += 1
            x += dx
            y += dy
            if x < 0 or x_limit < x or y < 0 or y_limit < y:
                break
            tile = map[y][x]
            if tile == FLOOR:
                continue
            elif tile == EMPTY_SEAT:
                break
            elif tile == OCCUPIED_SEAT:
                return False
    return True


def is_surrounding_crowded(
    start_x, start_y, map, x_limit, y_limit, tolerance, max_steps
):
    surrounding_occupied = 0
    for direction in DIRECTIONS:
        step = 0
        x, y = start_x, start_y
        while not max_steps or step < max_steps:
            step += 1
            x += direction[0]
            y += direction[1]
            if x < 0 or x_limit < x or y < 0 or y_limit < y:
                break
            tile = map[y][x]
            if tile == FLOOR:
                continue
            elif tile == EMPTY_SEAT:
                break
            elif tile == OCCUPIED_SEAT:
                surrounding_occupied += 1
                break
        if surrounding_occupied > tolerance:
            return True
    return False


def tick(map, tolerance, x_limit, y_limit, max_steps=False):
    change = False
    next_map = [[tile for tile in row] for row in map]

    for y, row in enumerate(map):
        for x, tile in enumerate(row):
            if tile == FLOOR:
                continue

            if tile == EMPTY_SEAT and is_all_surrounding_free(
                x, y, map, x_limit, y_limit, max_steps
            ):
                next_map[y][x] = OCCUPIED_SEAT
                change = True

            elif tile == OCCUPIED_SEAT and is_surrounding_crowded(
                x, y, map, x_limit, y_limit, tolerance, max_steps
            ):
                next_map[y][x] = EMPTY_SEAT
                change = True
    return next_map, change


def main():
    path = "advent_of_code/2020/advent_of_code_day11/input.txt"
    map = parse_input(path)
    x_limit = len(map[0]) - 1
    y_limit = len(map) - 1

    change = True
    while change:
        map, change = tick(map, 3, x_limit, y_limit, max_steps=1)
    print(f"Part 1: {count_occupied_seats(map)}")

    map = parse_input(path)

    change = True
    while change:
        map, change = tick(map, 4, x_limit, y_limit)
    print(f"Part 2: {count_occupied_seats(map)}")


if __name__ == "__main__":
    cProfile.run("main()", sort="cumtime")
    # main()
