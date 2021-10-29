from os import error
from pathlib import Path
from pydantic import BaseModel, ValidationError, validator
import re


class TolerantPassport(BaseModel):
    byr: str
    iyr: str
    eyr: str
    hgt: str
    hcl: str
    ecl: str
    pid: str
    cid: str = None


class StrictPassport(TolerantPassport):
    @validator("byr")
    def byr_is_valid(cls, byr: str) -> str:
        lower_limit = 1920
        upper_limit = 2002
        match = re.match(r"^\d{4}$", byr)
        if match and _in_range(int(byr), lower_limit, upper_limit):
            return byr
        else:
            raise ValueError("Must be 4 digits")

    @validator("iyr")
    def iyr_is_valid(cls, iyr: str) -> str:
        lower_limit = 2010
        upper_limit = 2020
        match = re.match(r"^\d{4}$", iyr)
        if match and _in_range(int(iyr), lower_limit, upper_limit):
            return iyr
        else:
            raise ValueError("Must be 4 digits")

    @validator("eyr")
    def eyr_is_valid(cls, eyr: str) -> str:
        lower_limit = 2020
        upper_limit = 2030
        match = re.match(r"^\d{4}$", eyr)
        if match and _in_range(int(eyr), lower_limit, upper_limit):
            return eyr
        else:
            raise ValueError("Must be 4 digits")

    @validator("hgt")
    def hgt_is_valid(cls, hgt: str) -> str:
        match = re.match(r"^(\d+)(in|cm)$", hgt)
        if match:
            length = int(match.group(1))
            unit = match.group(2)

            if unit == "cm":
                if _in_range(length, 150, 193):
                    return hgt

            elif unit == "in":
                if _in_range(length, 59, 76):
                    return hgt

            raise ValueError("Legnth not in the required range.")

        else:
            raise ValueError("Input not as excpected.")

    @validator("hcl")
    def hcl_is_valid(cls, hcl: str) -> str:
        if re.match(r"^#[0-9a-f]{6}$", hcl):
            return hcl
        else:
            raise ValueError(f"Haircolor must be a Hex value, got {hcl}")

    @validator("pid")
    def pid_is_valid(cls, pid: str) -> str:
        if re.match(r"^\d{9}$", pid):
            return pid
        else:
            raise ValueError(f"Passport ID must be a 9 digit value, got {pid}")

    @validator("ecl")
    def ecl_is_valid(cls, ecl: str) -> str:
        allowed_set = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
        if ecl not in allowed_set:
            raise ValueError(f"Eyecolor must be one of {allowed_set}, got '{ecl}'")
        return ecl


def _in_range(value: int, lower_limit: int, upper_limit: int):
    return lower_limit <= value <= upper_limit


def parse_input(path: Path):

    input = path.read_text().split("\n\n")

    passport_list = []
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
    passport_list = parse_input(Path("school_of_code/advent_of_code_day4/input.txt"))

    # Part 1
    valid_passports = []
    for passport in passport_list:
        try:
            valid_passports.append(TolerantPassport(**passport))
        except ValidationError as e:
            pass

    print(f"Part 1: Valid passports: {len(valid_passports)}")

    # Part 2
    valid_passports = []
    for passport in passport_list:
        try:
            valid_passports.append(StrictPassport(**passport))
        except ValidationError as e:
            pass

    print(f"Part 2: Valid passports: {len(valid_passports)}")


if __name__ == "__main__":
    main()
