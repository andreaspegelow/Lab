from dataclasses import dataclass
from pathlib import Path
import random
import cProfile
from time import time
import datetime


@dataclass
class Instruction:
    command: str
    a: str
    b: str


@dataclass
class Storage:
    w: int = 0
    x: int = 0
    y: int = 0
    z: int = 0

    def __hash__(self) -> int:
        return (self.w + 3) * (self.y + 7) * (self.x + 21) * (self.z + 11)


def inp(a: str, b: int, storage: Storage):
    if a == "w":
        storage.w = b
    elif a == "x":
        storage.x = b
    elif a == "y":
        storage.y = b
    elif a == "z":
        storage.z = b
    return storage


def add(a: str, b: str, storage: Storage):
    try:
        b = int(b)
    except ValueError:
        b = eval(f"storage.{b}")
    if a == "w":
        storage.w = storage.w + b
    elif a == "x":
        storage.x = storage.x + b
    elif a == "y":
        storage.y = storage.y + b
    elif a == "z":
        storage.z = storage.z + b
    return storage


def mul(a: str, b: str, storage: Storage):
    try:
        b = int(b)
    except ValueError:
        b = eval(f"storage.{b}")

    if a == "w":
        storage.w = storage.w * b
    elif a == "x":
        storage.x = storage.x * b
    elif a == "y":
        storage.y = storage.y * b
    elif a == "z":
        storage.z = storage.z * b
    return storage


def div(a: str, b: str, storage: Storage):
    try:
        b = int(b)
    except ValueError:
        b = eval(f"storage.{b}")
    if a == "w":
        storage.w = int(storage.w / b)
    elif a == "x":
        storage.x = int(storage.x / b)
    elif a == "y":
        storage.y = int(storage.y / b)
    elif a == "z":
        storage.z = int(storage.z / b)
    return storage


def mod(a: str, b: str, storage: Storage):
    try:
        b = int(b)
    except ValueError:
        b = eval(f"storage.{b}")
    if a == "w":
        storage.w = storage.w % b
    elif a == "x":
        storage.x = storage.x % b
    elif a == "y":
        storage.y = storage.y % b
    elif a == "z":
        storage.z = storage.z % b
    return storage


def eql(a: str, b: str, storage: Storage):
    try:
        b = int(b)
    except Exception:
        b = eval(f"storage.{b}")
    if a == "w":
        storage.w = 1 if storage.w == b else 0
    elif a == "x":
        storage.x = 1 if storage.x == b else 0
    elif a == "y":
        storage.y = 1 if storage.y == b else 0
    elif a == "z":
        storage.z = 1 if storage.z == b else 0
    return storage


def parse_input(path):
    instructions = []
    lines = Path(path).read_text().split("\n")
    for line in lines:
        command, value = line.split(" ", 1)
        if command == "inp":
            instructions.append(Instruction(inp, value, None))
            continue
        elif command == "add":
            command = add
        elif command == "mul":
            command = mul
        elif command == "div":
            command = div
        elif command == "mod":
            command = mod
        elif command == "eql":
            command = eql
        a, b = value.split(" ")
        instructions.append(Instruction(command, a, b))

    return instructions


def interpeter(input_number: int, z: int, instructions: list):
    storage = Storage(z=z)
    # if len(str(input_number)) != len(
    #     [instruction for instruction in instructions if instruction.command == inp]
    # ):
    #     raise ValueError("Input number not correct length.")

    for instruction in instructions:
        if instruction.command == inp:
            temp = list(str(input_number))
            instruction.b = int(temp.pop(0))
            if temp != []:
                input_number = int("".join(temp))
        storage = instruction.command(instruction.a, instruction.b, storage)
    return storage


def main():

    start_time = time()
    blocks = parse_input("advent_of_code/2021/advent_of_code_day24/input.txt")
    if (
        Path("advent_of_code/2021/advent_of_code_day24/tested_numbers.txt").read_text()
        == ""
    ):
        possible_solutions = ""
        tested_numbers = ""
    else:
        possible_solutions, tested_numbers = (
            Path("advent_of_code/2021/advent_of_code_day24/tested_numbers.txt")
            .read_text()
            .split("\n")
        )
    lowest_z = (9999999999, 11111111111111)
    if possible_solutions != "":
        possible_solutions = set([int(i) for i in possible_solutions.split(",")])
    else:
        possible_solutions = set()
    if tested_numbers != "":
        tested_numbers = set([int(i) for i in tested_numbers.split(",")])
    else:
        tested_numbers = set()
    time_saves = 0
    print("Starting...")
    while True:
        # for random_number in range(99999999999999,1,-1):
        while True:
            random_number = random.randint(
                (
                    max(possible_solutions)
                    if possible_solutions != set()
                    else 11111111111111
                ),
                99999999999999,
            )
            if str(random_number).count("0") > 0:
                continue
            if random_number in tested_numbers:
                time_saves += 1
                continue
            tested_numbers.add(random_number)
            new_storage = interpeter(random_number, 0, blocks)
            if new_storage.z < lowest_z[0] and new_storage.z != 0:
                lowest_z = (new_storage.z, random_number)
            if new_storage.z < 999:
                if new_storage.z == 0:
                    print(f"Possible solution? {random_number}")
                    possible_solutions.add(random_number)
                print(f"Selecting: {new_storage.z} {random_number}")
                break
            # if random_number % 4567 == 0:
            #     save(possible_solutions, tested_numbers, start_time)

        random_number_copy = str(random_number)
        last_z = new_storage.z
        for _ in range(999):
            random_pos = random.randint(0, 13)
            random_digit = random.randint(1, 9)
            random_number_copy = str(random_number_copy)
            random_number_copy = (
                random_number_copy[:random_pos]
                + str(random_digit)
                + random_number_copy[random_pos + 1 :]
            )
            random_number_copy = int(random_number_copy)
            if random_number_copy in tested_numbers:
                continue
            if random_number_copy < (
                max(possible_solutions)
                if possible_solutions != set()
                else 11111111111111
            ):
                continue
            tested_numbers.add(random_number_copy)
            new_storage = interpeter(random_number_copy, 0, blocks)
            if new_storage.z < lowest_z[0] and new_storage.z != 0:
                lowest_z = (new_storage.z, random_number_copy)
            if new_storage.z == 0:
                print(f"Possible solution? {random_number_copy}")
                possible_solutions.add(random_number_copy)
                break
            if new_storage.z < last_z:
                last_z = new_storage.z
                random_number = random_number_copy
            else:
                random_number_copy = str(random_number)

        print("No solution. Trying again....")
        print(f"Tested numbers: {len(tested_numbers)}")
        print(
            f"Number of possible solutions found: {len(possible_solutions)} {possible_solutions}"
        )
        print(f"Number of time saves: {time_saves}")
        print(f"So far lowest z found: {lowest_z}")
        save(possible_solutions, tested_numbers, start_time)
        print("-" * 80)


def save(possible_solutions, tested_numbers, start_time):
    print("Saving.")
    with open(
        "advent_of_code/2021/advent_of_code_day24/tested_numbers.txt", "w"
    ) as file:
        file.write(",".join([str(i) for i in possible_solutions]))
        file.write("\n")
        # file.write(",".join([str(i) for i in tested_numbers]))
    print("Done saving.")
    print(f"{datetime.datetime.now()} Have been running for: {time()-start_time:.0f}s")
    prom =[71981795537981,71431792216861,61871793326871] 
   


if __name__ == "__main__":
    main()
    # cProfile.run("main()")
