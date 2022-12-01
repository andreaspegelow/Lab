import os

for i in range (1,26):
    folder_path = f"advent_of_code/2022/advent_of_code_day{i}"
    os.mkdir(folder_path)
    with open(f"{folder_path}/advent_of_code_day{i}.py", "w") as file:
        file.write(f'from pathlib import Path\nfrom typing import List\n\n\ndef parse_input(path: str) -> List[int]:\n    return [int(i) for i in Path(path).read_text().split("\\n")]\n\n\ndef main():\n    puzzle_input = parse_input("advent_of_code/2022/advent_of_code_day{i}/input.txt")\n\n\nif __name__ == "__main__":\n    main()\n')
    with open(f"{folder_path}/input.txt", "w") as file:
        pass