from pathlib import Path
from typing import List


def parse_input(path: str) -> List[int]:
    return [int(i) for i in Path(path).read_text().split("\n")]


def main():
    input = parse_input("advent_of_code/2019/advent_of_code_day1/input.txt")

    result = sum(module_mass // 3 - 2 for module_mass in input)
    print(f"Part 1: {result}")

    result = sum(calculate_fuel(module_mass) for module_mass in input)
    print(f"Part 2: {result}")


def calculate_fuel(mass: int) -> int:
    fuel = mass // 3 - 2
    return fuel + calculate_fuel(fuel) if fuel > 0 else 0


if __name__ == "__main__":
    main()
