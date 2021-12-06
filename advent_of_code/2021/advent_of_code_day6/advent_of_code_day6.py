from pathlib import Path


def parse_input(path: str):
    return [int(i) for i in Path(path).read_text().split(",")]


def simulate_evolution(fishes, days):
    fish_map = {}
    for i in range(9):
        fish_map[i] = fishes.count(i)

    for i in range(days):
        new_fishes_to_add = fish_map[0]
        for i in range(1, 9):
            fish_map[i - 1] = fish_map[i]
        fish_map[6] = fish_map[6] + new_fishes_to_add
        fish_map[8] = new_fishes_to_add

    return sum(fish_map.values())


def main():
    fishes = parse_input("advent_of_code/2021/advent_of_code_day6/input.txt")
    number_of_fishes = simulate_evolution(fishes, 80)
    print(f"Part 1: {number_of_fishes}")

    number_of_fishes = simulate_evolution(fishes, 256)
    print(f"Part 2: {number_of_fishes}")


if __name__ == "__main__":
    main()
