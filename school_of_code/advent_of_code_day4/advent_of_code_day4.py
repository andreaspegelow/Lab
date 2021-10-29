from pathlib import Path


def parse_input(path: Path) -> list:
    passport_list = []
    input = path.read_text().split("\n\n")

    for passport in input:
        passport = passport.replace("\n", " ")
        passport = passport.split(" ")
        passport_dict = {}
        for key_value_pair in passport:
            key_value_pair = key_value_pair.split(":")
            passport_dict[key_value_pair[0]] = key_value_pair[1]
        passport_list.append(passport_dict)

    return passport_list


def main():

    required_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    optional_fields = ["cid"]
    passport_list = parse_input(Path("school_of_code/advent_of_code_day4/input.txt"))

    number_of_valid_passport = 0
    for passport in passport_list:
        key_list = {key for key in passport.keys()}
        diff = required_fields - key_list
        if diff:
            if len(diff) == 1 and diff in optional_fields:
                 number_of_valid_passport +=1
        else:
            number_of_valid_passport +=1

    print(number_of_valid_passport)
            


if __name__ == "__main__":
    main()
