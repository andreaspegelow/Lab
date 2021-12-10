from pathlib import Path


def parse_input(path: str):

    rows = Path(path).read_text().split("\n")
    instructions = []
    for row in rows:
        input, output = row.split("|")
        input = input.strip().split(" ")
        output = output.strip().split(" ")
        instructions.append((input, output))
    return instructions


def main():
    instructions = parse_input("advent_of_code/2021/advent_of_code_day8/input.txt")
    count = 0
    for instruction in instructions:
        for output in instruction[1]:
            if len(output) in [2, 3, 4, 7]:
                count += 1
    print(f"Part 1: {count}")

    count = 0
    for instruction in instructions:
        number_dict = {}
        for input in instruction[0]:
            if len(input) == 2:
                number_dict[1] = set(input)
            if len(input) == 3:
                number_dict[7] = set(input)
            if len(input) == 4:
                number_dict[4] = set(input)
            if len(input) == 7:
                number_dict[8] = set(input)

        for input in instruction[0]:
            if len(input) == 6:
                if len(set(input) - number_dict[4]) == 2:
                    number_dict[9] = set(input)
                else:
                    if len(set(input) - number_dict[1]) == 4:
                        number_dict[0] = set(input)
                    else:
                        number_dict[6] = set(input)
            if len(input) == 5:
                if len(set(input) - number_dict[1]) == 3:
                    number_dict[3] = set(input)
                else:
                    if len(set(input) - number_dict[4]) == 3:
                        number_dict[2] = set(input)
                    else:
                        number_dict[5] = set(input)
        output = ""
        for input_signal in instruction[1]:
            for digit, signal_map in number_dict.items():
                if set(input_signal) == signal_map:
                    output += str(digit)
        count += int(output)

    print(f"Part 2: {count}")


if __name__ == "__main__":
    main()
