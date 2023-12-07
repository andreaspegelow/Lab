from pathlib import Path
from typing import List
import time

seed_to_soil_map = []
soil_to_fertilizer_map = []
fertilizer_to_water = []
water_to_light_map = []
light_to_temperature_map = []
temperature_to_humidity_map = []
humidity_to_location_map = []


def parse_input(path: str) -> List[int]:
    return Path(path).read_text().split("\n")


def seconds_to_string(input_seconds):
    result = ""
    min, seconds = divmod(input_seconds, 60)
    hours, min = divmod(min, 60)
    if hours > 0:
        result += f"{int(hours)}h:"
    if min > 0 or hours > 0:
        result += f"{int(min)}m:"

    result += f"{round(seconds,2)}s"
    return result


def in_range(value, range: range):
    return range.start <= value < range.stop


def convert(source, map):
    for source_range_start, dest_range_start, range_length in map:
        if source >= source_range_start and source < source_range_start + range_length:
            return dest_range_start + source - source_range_start
    return source


def convert_reversed(destination, map):
    for source_range_start, dest_range_start, range_length in map:
        if dest_range_start <= destination < dest_range_start + range_length:
            return source_range_start + destination - dest_range_start
    return destination


def seed_to_location(seed):
    location = convert(seed, seed_to_soil_map)
    location = convert(location, soil_to_fertilizer_map)
    location = convert(location, fertilizer_to_water)
    location = convert(location, water_to_light_map)
    location = convert(location, light_to_temperature_map)
    location = convert(location, temperature_to_humidity_map)
    location = convert(location, humidity_to_location_map)
    return location


def location_to_seed(location):
    location = convert_reversed(location, humidity_to_location_map)
    location = convert_reversed(location, temperature_to_humidity_map)
    location = convert_reversed(location, light_to_temperature_map)
    location = convert_reversed(location, water_to_light_map)
    location = convert_reversed(location, fertilizer_to_water)
    location = convert_reversed(location, soil_to_fertilizer_map)
    location = convert_reversed(location, seed_to_soil_map)
    return location


def location_in_seed_ranges(location, seed_ranges):
    return any(
        [in_range(location_to_seed(location), seed_range) for seed_range in seed_ranges]
    )


def main():
    puzzle_input = parse_input(
        "advent_of_code/2023/advent_of_code_day5/input_small.txt"
    )
    puzzle_input = parse_input("advent_of_code/2023/advent_of_code_day5/input.txt")
    seeds = list(map(int, puzzle_input[0].split(":")[1].split()))

    target = None
    for line in puzzle_input[2:]:
        if "seed-to-soil map" in line:
            target = seed_to_soil_map
            continue
        elif "soil-to-fertilizer map" in line:
            target = soil_to_fertilizer_map
            continue
        elif "fertilizer-to-water map" in line:
            target = fertilizer_to_water
            continue
        elif "water-to-light map" in line:
            target = water_to_light_map
            continue
        elif "light-to-temperature map" in line:
            target = light_to_temperature_map
            continue
        elif "temperature-to-humidity map" in line:
            target = temperature_to_humidity_map
            continue
        elif "humidity-to-location map" in line:
            target = humidity_to_location_map
            continue

        if line == "":
            target = None
            continue

        dest_range_start, source_range_start, range_length = map(int, line.split())
        target.append((source_range_start, dest_range_start, range_length))

    closest = None
    for seed in seeds:
        location = seed_to_location(seed)
        if not closest or location < closest:
            closest = location
    print(f"Part 1: {closest}")

    seed_ranges = []
    for i in range(0, len(list(seeds)), 2):
        start, length = seeds[i], seeds[i + 1]
        seed_ranges.append(range(start, start + length))

    max = 26714517
    start_time = time.perf_counter()
    for location in range(max):
        if location % 10000 == 0:
            elapsed_time = time.perf_counter() - start_time
            average_time = elapsed_time / (location + 1)
            remaining_iterations = max - (location + 1)
            progress = round((location / max * 100), 1)
            print(
                f"\r{progress}% Estimated remaning time: {seconds_to_string( average_time* remaining_iterations)}",
                end="",
            )
        if location_in_seed_ranges(location, seed_ranges):
            print(f"Part 2: {location}")
            break


if __name__ == "__main__":
    main()
