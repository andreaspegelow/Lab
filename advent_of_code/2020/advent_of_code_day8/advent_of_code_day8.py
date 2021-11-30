from dataclasses import dataclass
from pathlib import Path
import copy


@dataclass
class Instruction:
    command: str
    value: int
    visited: bool = False


def acc(PC, value, acc):
    return PC + 1, acc + value


def jmp(PC, value, acc):
    return PC + value, acc


def nop(PC, value, acc):
    return PC + 1, acc


class InfLoopException(Exception):
    pass


def parse_input(path):
    instructions = []
    input = Path(path).read_text().split("\n")
    for line in input:
        command, value = line.split(" ")
        if command == "acc":
            command = acc
        if command == "jmp":
            command = jmp
        if command == "nop":
            command = nop
        instructions.append(Instruction(command, int(value)))
    return instructions


def interpeter(instructions):
    accumulator = 0
    pc = 0
    while True:
        try:
            instruction = instructions[pc]
        except IndexError:
            return accumulator

        if not instruction.visited:
            pc, accumulator = instruction.command(pc, instruction.value, accumulator)
            instruction.visited = True
        else:
            raise InfLoopException(f"InfLoopException, accumulator is: {accumulator}")


def main():

    # Part 1
    instructions = parse_input("advent_of_code/2020/advent_of_code_day8/input.txt")
    try:
        interpeter(instructions)
    except InfLoopException as e:
        print(e)

    # Part 2
    instructions = parse_input("advent_of_code/2020/advent_of_code_day8/input.txt")
    instructions_copy = instructions
    for i, instruction in enumerate(instructions):

        instructions_copy = copy.deepcopy(instructions)

        if instruction.command == nop:
            instructions_copy[i] = Instruction(jmp, instruction.value)
        elif instruction.command == jmp:
            instructions_copy[i] = Instruction(nop, instruction.value)
        elif instruction.command == acc:
            continue

        try:
            result = interpeter(instructions_copy)
        except InfLoopException as e:
            pass
        else:
            print(f"Found a correct solution by changing instruction in index: {i}! Accumulator is: {result}")
            break


if __name__ == "__main__":
    main()
