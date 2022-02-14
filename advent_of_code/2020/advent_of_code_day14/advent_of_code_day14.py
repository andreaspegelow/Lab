from pathlib import Path
from itertools import product


def parse_input(path: Path):
    input = []
    for line in Path(path).read_text().split("\n"):
        opperation, value = (
            line.replace(" ", "").replace("mem[", "").replace("]", "").split("=")
        )
        input.append((opperation, value))
    return input


def main():
    path = Path("advent_of_code/2020/advent_of_code_day14/input.txt")
    input = parse_input(path)
    current_mask = None
    memory = {}
    for opperation, value in input:
        if opperation == "mask":
            current_mask = value
        else:
            mask = int(current_mask.replace("X", "1"), 2)
            new_value = int(value) & mask

            mask = int(current_mask.replace("X", "0"), 2)
            new_value = new_value | mask
            memory[opperation] = new_value

    print(f"Part 1: {sum(memory.values())}")

    current_mask = None
    memory = {}
    for opperation, value in input:
        if opperation == "mask":
            current_mask = value
        else:
            addres = int(opperation)
            mask = int(current_mask.replace("X", "1"), 2)
            addres = addres | mask

            for premutation in range(2 ** current_mask.count("X")):
                premutation = list(bin(premutation)[2:].zfill(36))
                new_address = list(bin(addres)[2:].zfill(36))
                for i, c in enumerate(current_mask):
                    if c == "X":
                        new_address[i] = str(premutation.pop())
                memory[int("".join(new_address), 2)] = int(value)

    print(f"Part 2: {sum(memory.values())}")


if __name__ == "__main__":
    main()
