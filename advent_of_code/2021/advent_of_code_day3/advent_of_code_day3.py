from pathlib import Path


def parse_input(path: str):
    return [i for i in Path(path).read_text().split("\n")]


def get_most_common_bit(number_list, bit_index):
    bit_sum = 0
    for number in number_list:
        bit_sum += int(number[bit_index])
    return "1" if bit_sum >= len(number_list) / 2 else "0"


def main():
    input = parse_input("advent_of_code/2021/advent_of_code_day3/input.txt")
    # Part 1
    result = ""
    for i in range(len(input[0])):
        result += get_most_common_bit(input, i)

    result_inverted = int("".join("1" if x == "0" else "0" for x in result), 2)
    result = int(result, 2)
    print(f"Part 1: {result * result_inverted}")

    # Part 2
    oxygen_generator_rating, CO2_scrubber_rating = -1, -1
    input_copy = input.copy()
    for i in range(len(input_copy[0])):
        most_common = get_most_common_bit(input_copy, i)
        input_copy = [j for j in input_copy if j[i] == most_common]
        if len(input_copy) == 1:
            oxygen_generator_rating = int(input_copy[0], 2)
            break

    input_copy = input.copy()
    for i in range(len(input_copy[0])):
        least_common = str(int(get_most_common_bit(input_copy, i)) * -1 + 1)
        input_copy = [j for j in input_copy if j[i] == least_common]
        if len(input_copy) == 1:
            CO2_scrubber_rating = int(input_copy[0], 2)
            break

    print(f"Part 2: {oxygen_generator_rating * CO2_scrubber_rating}")


if __name__ == "__main__":
    main()
