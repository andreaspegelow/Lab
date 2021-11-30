import math
import sys
import datetime


def parse_input(path: str) -> list:
    input = []
    with open(path) as f:
        lines = f.readlines()
        for line in lines:
            input.append(int(line.replace("\n", "")))
    return input

def find_factors(sum: int, input: list, number_of_factors) -> list:

    to_look_into_fast = set(input)

    if number_of_factors < 2:
        sys.exit(1)
    for i, number1 in enumerate(input):

        if number1 >= sum:
            continue

        number_to_find = sum - number1
        if number_of_factors == 2:
            if number_to_find in to_look_into_fast:
                number2 = number_to_find
                return [number1, number2]
        else:
            input.remove(number1)
    
            if (result := find_factors(number_to_find, input, number_of_factors - 1)):
                return [number1] + result

    return []


def main():
    input = parse_input("advent_of_code/2020/advent_of_code_day1/input.txt")
    sum = 2020

    # Part 1
    number_of_factors = 2
    t1 = datetime.datetime.now()
    result = find_factors(sum, input, number_of_factors)
    print(f"Time diff fast: {datetime.datetime.now() - t1}")
    if result:
        print(
            f"Part1: Found the entries: {result} which sum to: {sum} and they have the product: {math.prod(result)}"
        )
    else:
        print(f"Could not find a solution for {number_of_factors} factors.")

    # Part 2
    number_of_factors = 3
    t1 = datetime.datetime.now()
    result = find_factors(sum, input, number_of_factors)
    print(f"Time diff fast: {datetime.datetime.now() - t1}")
    if result:
        print(
            f"Part2: Found the entries: {result} which sum to: {sum} and they have the product: {math.prod(result)}"
        )
    else:
        print(f"Could not find a solution for {number_of_factors} factors.")


if __name__ == "__main__":
    main()
