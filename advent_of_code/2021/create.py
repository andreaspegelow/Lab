import os

for i in range (2,26):
    folder_path = f"advent_of_code/2021/advent_of_code_day{i}"
    os.mkdir(folder_path)
    with open(f"{folder_path}/advent_of_code_day{i}.py", "w") as file:
        file.write(f'from pathlib import Path\n\n\ndef parse_input(path: str):\n\treturn [int(i) for i in Path(path).read_text().split("\\n")]\n\n\ndef main():\n\tinput = parse_input("advent_of_code/2021/advent_of_code_day{i}/input.txt")\n\n\nif __name__ == "__main__":\n\tmain()\n')
    with open(f"{folder_path}/input.txt", "w") as file:
        pass