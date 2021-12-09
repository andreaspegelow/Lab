from pathlib import Path


def parse_input(path: str):
    input = [int(i) for i in Path(path).read_text().split(",")]
    return {i: input.count(i) for i in range(max(input) + 1) if input.count(i) != 0}


def simple_fuel_calculation_method(dist):
    return dist


def advanced_fuel_calculation_method(dist):
    return int((dist * (dist + 1)) / 2)


def calculate_fuel_cost(crab_dict: dict, fuel_calculation_method: callable):
    cheapest_post_cost = 9999999999999999

    for target_pos in range(max(crab_dict.keys()) + 1):
        accumelated_cost = 0
        for current_position, number_of_crabs in crab_dict.items():
            dist = abs(current_position - target_pos)
            accumelated_cost += fuel_calculation_method(dist) * number_of_crabs
            if accumelated_cost > cheapest_post_cost:
                break
        else:
            cheapest_post_cost = accumelated_cost

    return cheapest_post_cost


def main():
    crab_dict = parse_input("advent_of_code/2021/advent_of_code_day7/input.txt")

    print(f"Part 1: {calculate_fuel_cost(crab_dict, simple_fuel_calculation_method)}")
    print(f"Part 2: {calculate_fuel_cost(crab_dict, advanced_fuel_calculation_method)}")


if __name__ == "__main__":
    main()
