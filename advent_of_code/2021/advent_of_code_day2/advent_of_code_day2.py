from pathlib import Path


def parse_input(path: str):
    return [i for i in Path(path).read_text().split("\n")]


def main():
    input = parse_input("advent_of_code/2021/advent_of_code_day2/input.txt")
    depth, horizontal = 0, 0
    for instruction in input:
        action, value = instruction.split(" ")
        value = int(value)
        if action == "down":
            depth += value
        elif action == "up":
            depth -= value
        elif action == "forward":
            horizontal += value
    print(depth * horizontal)

    input = parse_input("advent_of_code/2021/advent_of_code_day2/input.txt")
    depth, horizontal, aim = 0, 0, 0
    for instruction in input:
        action, value = instruction.split(" ")
        value = int(value)
        if action == "down":
            aim += value
        elif action == "up":
            aim -= value
        elif action == "forward":
            horizontal += value
            depth += aim * value
    print(depth * horizontal)


if __name__ == "__main__":
    main()
