from pathlib import Path


def parse_input(path: str):
    return [int(i) for i in Path(path).read_text().split("\n")]


def main():
    input = parse_input("advent_of_code/2021/advent_of_code_day1/input.txt")
    
    count = 0
    for i in range(1, len(input)):
        if input[i] > input[i - 1]:
            count += 1
    print(count)

    count = 0
    for i in range(3, len(input)):
        if sum(input[i - 3 : i]) > sum(input[i - 4 : i - 1]):
            count += 1
    print(count)

    count = 0
    for a, b in zip(input, input[1:]):
        if a < b:
            count += 1
    print(count)

    count = 0
    for a, b, c, d in zip(input, input[1:], input[2:], input[3:]):
        if a + b + c < b + c + d:
            count += 1
    print(count)


if __name__ == "__main__":
    main()
