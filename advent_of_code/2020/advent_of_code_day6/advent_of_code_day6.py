from pathlib import Path


def main():
    groups_answers = (
        Path("advent_of_code/2020/advent_of_code_day6/input.txt").read_text().split("\n\n")
    )

    count = 0
    for group_answers in groups_answers:
        count += len(set(group_answers.replace("\n", "")))

    print(f"Part 1: {count}")

    count = 0
    for group_answers in groups_answers:
        answer_set = [set(answer) for answer in group_answers.split("\n")]
        count += len(set.intersection(*answer_set))

    print(f"Part 2: {count}")


if __name__ == "__main__":
    main()
