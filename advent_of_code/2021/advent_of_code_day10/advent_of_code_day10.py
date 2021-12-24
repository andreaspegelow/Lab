from pathlib import Path


def parse_input(path: str):
    return Path(path).read_text().split("\n")


def main():
    syntax_score_map = {">": 25137, ")": 3, "]": 57, "}": 1197}
    autocomplete_score_map = {"<": 4, "(": 1, "[": 2, "{": 3}

    lines = parse_input("advent_of_code/2021/advent_of_code_day10/input.txt")

    syntax_score = 0
    autocomplete_scores = []
    for line in lines:
        prev = len(line) + 1
        while len(line) < prev:
            prev = len(line)
            for pair in ["()", "<>", "[]", "{}"]:
                line = line.replace(pair, "")

        if len(set(syntax_score_map.keys()).intersection(set(line))) > 0:
            # Corrupt
            for car in line:
                if car in syntax_score_map.keys():
                    syntax_score += syntax_score_map[car]
                    break
        else:
            # Incomplete
            autocomplete_score = 0
            for car in line[::-1]:
                autocomplete_score = (
                    autocomplete_score * 5 + autocomplete_score_map[car]
                )
            autocomplete_scores.append(autocomplete_score)

    print(f"Part 1: {syntax_score}")
    autocomplete_scores.sort()
    print(f"Part 2: {autocomplete_scores[int(len(autocomplete_scores)/2)]}")


if __name__ == "__main__":
    main()
