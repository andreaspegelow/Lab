from pathlib import Path


def main():
    boarding_pass_list = (
        Path("school_of_code/advent_of_code_day5/input.txt").read_text().split("\n")
    )
    occupied_seat_ids = set()

    for boarding_pass in boarding_pass_list:

        remaining_possible_rows = [i for i in range(128)]
        for letter_pos in range(0, 7):
            length = len(remaining_possible_rows)
            if boarding_pass[letter_pos] == "F":
                del remaining_possible_rows[length // 2 : length]
            elif boarding_pass[letter_pos] == "B":
                del remaining_possible_rows[0 : length // 2]

        remaining_possible_columns = [i for i in range(8)]
        for letter_pos in range(7, 10):
            length = len(remaining_possible_columns)
            if boarding_pass[letter_pos] == "L":
                del remaining_possible_columns[length // 2 : length]
            elif boarding_pass[letter_pos] == "R":
                del remaining_possible_columns[0 : length // 2]

        occupied_seat_ids.add(
            remaining_possible_rows[0] * 8 + remaining_possible_columns[0]
        )

    print(f"Part 1: {max(occupied_seat_ids)}")

    existing_seat_ids = {i * 8 + j for j in range(8) for i in range(128)}

    available_seat_ids = existing_seat_ids - occupied_seat_ids

    current = -1
    next = available_seat_ids.pop()
    while (next - 1) == current:
        current = next
        next = available_seat_ids.pop()
    print(f"Part 2: {next}")


if __name__ == "__main__":
    main()
