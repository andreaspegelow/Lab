from pathlib import Path
from functools import reduce


def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def main():
    path = "advent_of_code/2020/advent_of_code_day13/input.txt"
    input = Path(path).read_text().split("\n")
    arrival = int(input[0])
    buses = [int(bus_id) for bus_id in input[1].split(",") if bus_id != "x"]

    next_departures = [(bus_id - (arrival % bus_id), bus_id) for bus_id in buses]

    shortest_wait = (float("inf"), 0)
    for waiting_time, bus_id in next_departures:
        if waiting_time < shortest_wait[0]:
            shortest_wait = (waiting_time, bus_id)

    print(f"Part 1: {shortest_wait[0]* shortest_wait[1]}")

    path = "advent_of_code/2020/advent_of_code_day13/input.txt"
    input = Path(path).read_text().split("\n")[1].split(",")

    # 0 = t + a2 % a1 = t + b2 % b1 =...

    buses = [int(bus_id) for bus_id in input if bus_id != "x"]
    offsets = [int(bus_id) - i for i, bus_id in enumerate(input) if bus_id != "x"]

    print(f"Part 2: {chinese_remainder(buses, offsets)}")

    #  Brute force
    sets = []
    limit = 99999999
    for bus_id, offset in buses:
        print(f"Bus id: {bus_id}")
        i = 1
        s = set()
        while i < limit:
            s.add(i * bus_id - offset)
            i += 1
        sets.append(s)

    intersection = set.intersection(*sets)
    print(f"Part 2: {intersection}")

    # Brute force slightly optimized.
    i = 0
    while True:
        i += buses[0][0]
        for bus_id, offset in buses[1:]:
            if i + offset % bus_id == 0:
                print(f"t: {i} id: {bus_id}")
            else:
                break
        else:
            print(f"Part 2: {i}")
            break


if __name__ == "__main__":
    main()
