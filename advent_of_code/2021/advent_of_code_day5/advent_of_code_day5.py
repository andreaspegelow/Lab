from pathlib import Path


def parse_input(path: str):
    return [i for i in Path(path).read_text().split("\n")]


def main():
    lines = parse_input("advent_of_code/2021/advent_of_code_day5/input.txt")

    coords = set()
    dublicates = set()
    for line in lines:
        start, end = line.split(" -> ")
        x1 = int(start.split(",")[0])
        y1 = int(start.split(",")[1])
        x2 = int(end.split(",")[0])
        y2 = int(end.split(",")[1])

        if x1 == x2:
            for i in range(min(y1, y2), max(y1, y2) + 1):
                coord_to_add = (x1, i)
                if coord_to_add not in coords:
                    coords.add(coord_to_add)
                else:
                    dublicates.add(coord_to_add)

        elif y1 == y2:
            for i in range(min(x1, x2), max(x1, x2) + 1):
                coord_to_add = (i, y1)
                if coord_to_add not in coords:
                    coords.add(coord_to_add)
                else:
                    dublicates.add(coord_to_add)
        else:
            for x, y in zip(
                range(
                    x1,
                    x2 + (1 if x1 - x2 < 0 else -1),
                    1 if x1 - x2 < 0 else -1,
                ),
                range(
                    y1,
                    y2 + (1 if y1 - y2 < 0 else -1),
                    1 if y1 - y2 < 0 else -1,
                ),
            ):
                coord_to_add = (x, y)
                if coord_to_add not in coords:
                    coords.add(coord_to_add)
                else:
                    dublicates.add(coord_to_add)

    print(len(dublicates))


if __name__ == "__main__":
    main()
