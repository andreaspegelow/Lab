def main():
    # Part 1
    valid_paswords_count = 0
    with open("advent_of_code/2020/advent_of_code_day2/input.txt") as f:
        lines = f.readlines()
        for line in lines:
            limits, letter, password = line.split(" ")
            lower_limit, upper_limit = limits.split("-")
            letter = letter[0]

            if int(lower_limit) <= password.count(letter) <= int(upper_limit):
                valid_paswords_count += 1

    print(f"Part 1: Number of valid passwords: {valid_paswords_count}")

    print("*" * 80)

    # Part 2
    valid_paswords_count = 0
    with open("advent_of_code/2020/advent_of_code_day2/input.txt") as f:
        lines = f.readlines()
        for line in lines:
            positions, letter, password = line.split(" ")
            position1, position2 = positions.split("-")
            letter = letter[0] 

            if (password[int(position1) - 1] == letter) != (
                password[int(position2) - 1] == letter
            ):
                valid_paswords_count += 1

    print(f"Part 2: Number of valid passwords: {valid_paswords_count}")


if __name__ == "__main__":
    main()
