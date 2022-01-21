from pathlib import Path
from dataclasses import dataclass
import math

NORTH = "N"
WEST = "W"
SOUTH = "S"
EAST = "E"
LEFT = "L"
RIGHT = "R"
FORWARD = "F"
DIRECTIONS = [(1, 0), (0, -1), (-1, 0), (0, 1)]


@dataclass
class Pos:
    x: int
    y: int


def parse_input(path: str):
    return [(i[:1], int(i[1:])) for i in Path(path).read_text().split("\n")]


def offset(pos, direction, value):
    value = abs(value)
    pos.x = pos.x + (direction[0] * value)
    pos.y = pos.y + (direction[1] * value)
    return pos


def sign(value):
    return -1 if value < 0 else 1


def rotate(pos, angle):
    angle = math.radians(angle)
    new_x = math.cos(angle) * pos.x - math.sin(angle) * pos.y
    new_y = math.sin(angle) * pos.x + math.cos(angle) * pos.y
    pos.x = round(new_x)
    pos.y = round(new_y)
    return pos


def main():
    instructions = parse_input("advent_of_code/2020/advent_of_code_day12/input.txt")
    current_pos = Pos(0, 0)
    current_direction = 0
    # dir = Pos(1, 0)

    for action, value in instructions:
        if action == NORTH:
            current_pos = offset(current_pos, DIRECTIONS[3], value)
        elif action == SOUTH:
            current_pos = offset(current_pos, DIRECTIONS[1], value)
        elif action == WEST:
            current_pos = offset(current_pos, DIRECTIONS[2], value)
        elif action == EAST:
            current_pos = offset(current_pos, DIRECTIONS[0], value)
        elif action == FORWARD:
            current_pos = offset(current_pos, DIRECTIONS[current_direction], value)
        elif action == LEFT:
            current_direction = current_direction + int(value / 90) * -1
        elif action == RIGHT:
            current_direction = current_direction + int(value / 90) * 1
            
        # elif action == LEFT:
        #     dir = rotate(dir, value)
        # elif action == RIGHT:
        #     dir = rotate(dir, -value)
        # elif action == FORWARD:
        #     current_pos = move(current_pos, (dir.x, dir.y), value)

        current_direction = current_direction % len(DIRECTIONS)

    print(f"Part 1: {abs(current_pos.x) + abs(current_pos.y)}")

    current_pos_WCS = Pos(0, 0)
    way_point_FCS = Pos(10, 1)

    for action, value in instructions:
        if action == NORTH:
            way_point_FCS = offset(way_point_FCS, DIRECTIONS[3], value)
        elif action == SOUTH:
            way_point_FCS = offset(way_point_FCS, DIRECTIONS[1], value)
        elif action == WEST:
            way_point_FCS = offset(way_point_FCS, DIRECTIONS[2], value)
        elif action == EAST:
            way_point_FCS = offset(way_point_FCS, DIRECTIONS[0], value)
        elif action == FORWARD:
            for _ in range(value):
                current_pos_WCS = offset(
                    current_pos_WCS, (sign(way_point_FCS.x), 0), way_point_FCS.x
                )
                current_pos_WCS = offset(
                    current_pos_WCS, (0, sign(way_point_FCS.y)), way_point_FCS.y
                )
        elif action == LEFT:
            way_point_FCS = rotate(way_point_FCS, value)
        elif action == RIGHT:
            way_point_FCS = rotate(way_point_FCS, -value)

    print(f"Part 2: {abs(current_pos_WCS.x) + abs(current_pos_WCS.y)}")


if __name__ == "__main__":
    main()
