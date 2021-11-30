from pathlib import Path


def parse_input(path: Path):
    return [int(i) for i in Path(path).read_text().split("\n")]


def is_valid(number: int, preamble: set):
    for i, prev_number in enumerate(preamble):
        if number - prev_number in preamble:
            return True
    return False


def main():
    input = parse_input("school_of_code/advent_of_code_day9/input.txt")
    for i in range(25, len(input)):
        if not is_valid(input[i], set(input[i - 25 : i])):
            invalid_number = input[i]
            print(f"Part 1: {invalid_number}")
            break

    for i in range(len(input)):
        for j in range(i + 2, len(input)):
            s = sum(input[i:j])
            if s == invalid_number:
                print(f"Part 2:{min(input[i:j]) + max(input[i:j])} {input[i:j] = } ")
                return
            if s > invalid_number:
                break


if __name__ == "__main__":
    main()
