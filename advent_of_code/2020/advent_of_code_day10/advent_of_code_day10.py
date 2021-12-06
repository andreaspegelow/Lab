from pathlib import Path


def parse_input(path: str):
    return [int(i) for i in Path(path).read_text().split("\n")]


def count_valid_tails(list, M={}):
    if len(list) == 1:
        return 1

    count = M.get(list[0], 0)
    if count != 0:
        # This node as already been calculated.
        return count

    for i, number in enumerate(list[1:]):
        if number - list[0] <= 3:
            count += count_valid_tails(list[i + 1 :], M)
        else:
            break

    M[list[0]] = count
    return count


def main():
    input = parse_input("advent_of_code/2020/advent_of_code_day10/input.txt")
    input.append(0)
    input.append(max(input) + 3)
    input.sort()
    one_diff = 0
    three_diff = 0
    for i in range(len(input) - 1):
        diff = input[i + 1] - input[i]
        if diff == 1:
            one_diff += 1
        elif diff == 3:
            three_diff += 1

    print(f"Part 1: {one_diff*three_diff}")

    input = parse_input("advent_of_code/2020/advent_of_code_day10/input.txt")
    input.append(0)
    input.append(max(input) + 3)
    input.sort()
    print(f"Part 2: {count_valid_tails(input)}")


if __name__ == "__main__":
    main()
