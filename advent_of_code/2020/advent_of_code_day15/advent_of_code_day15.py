from pathlib import Path
import cProfile


def parse_input(path: str):
    return [int(i) for i in Path(path).read_text().split(",")]


def main():

    numbers_spoken = parse_input("advent_of_code/2020/advent_of_code_day15/input.txt")

    for i in range(len(numbers_spoken), 2020):
        last_spoken_number = numbers_spoken[-1]
        try:
            last_occurrence = (
                len(numbers_spoken)
                - 1
                - numbers_spoken[:-1][::-1].index(last_spoken_number)
            )
            numbers_spoken.append(i - last_occurrence)
        except ValueError:
            numbers_spoken.append(0)

    print(f"Part 1: {numbers_spoken[-1]}")

    start_numbers = parse_input("advent_of_code/2020/advent_of_code_day15/input.txt")
    numbers_spoken = {number: i + 1 for i, number in enumerate(start_numbers[:-1])}

    last_spoken_number = start_numbers[-1]
    for i in range(len(start_numbers), 30000000):
        try:
            number_to_speak = i - numbers_spoken[last_spoken_number]
        except KeyError:
            number_to_speak = 0

        numbers_spoken[last_spoken_number] = i
        last_spoken_number = number_to_speak

    print(f"Part 2: {last_spoken_number}")


if __name__ == "__main__":
    # cProfile.run("main()", sort="cumtime")
    main()
