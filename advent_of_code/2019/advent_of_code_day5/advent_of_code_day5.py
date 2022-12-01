import itertools
from copy import copy
from operator import add, mul
from pathlib import Path
from typing import List


def parse_input(path: str) -> List[int]:
    return [int(i) for i in Path(path).read_text().split(",")]


def run_program(memory, noun, verb):
    memory[1] = noun
    memory[2] = verb

    for pointer in range(0, len(memory), 4):
        opcode = memory[pointer]
        if opcode == 1:
            memory[memory[pointer + 3]] = add(
                memory[memory[pointer + 1]], memory[memory[pointer + 2]]
            )
        elif opcode == 2:
            memory[memory[pointer + 3]] = mul(
                memory[memory[pointer + 1]], memory[memory[pointer + 2]]
            )
        elif opcode == 3:
            memory[memory[pointer + 3]] = mul(
                memory[memory[pointer + 1]], memory[memory[pointer + 2]]
            )
        elif opcode == 99:
            return memory[0]
        else:
            # Error!
            return None


def main():
    input_memory = parse_input("advent_of_code/2019/advent_of_code_day5/input.txt")
    for noun, verb in itertools.product(range(99), range(99)):
        if (
            output := run_program(copy(input_memory), noun, verb)
        ) and output == 19690720:
            print(f"Done! Result: {100 * noun + verb}")


if __name__ == "__main__":
    main()
