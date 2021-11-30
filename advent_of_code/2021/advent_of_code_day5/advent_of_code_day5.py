from pathlib import Path


def parse_input(path: str):
	input = Path(path).read_text().split("\n")
	for line in input:
		line = line
		return input


def main():
	input = parse_input("advent_of_code/2021/advent_of_code_day5/input.txt")


if __name__ == "__main__":
	main()
