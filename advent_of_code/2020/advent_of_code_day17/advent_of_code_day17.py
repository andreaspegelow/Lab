from pathlib import Path


def parse_input(path: str):
	return [int(i) for i in Path(path).read_text().split("\n")]


def main():
	input = parse_input("advent_of_code/2020/advent_of_code_day17/input.txt")


if __name__ == "__main__":
	main()
