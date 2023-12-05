from pathlib import Path
from typing import List


def parse_input(path: str) -> List[int]:
    return Path(path).read_text().split("\n")


def winns(card):
    winning_numbers = card.split(" | ")[0].split(":")[1].split()
    your_numbers = card.split(" | ")[1].split()
    return len(set(winning_numbers) & set(your_numbers))


def main():
    puzzle_input = parse_input("advent_of_code/2023/advent_of_code_day4/input.txt")

    total = sum(
        [2 ** (winnings - 1) for card in puzzle_input if (winnings := winns(card))]
    )

    print(f"Part 1: {total}")

    cards = {i: 1 for i in range(len(puzzle_input))}
    for card_index, count in cards.items():
        for i in range(winns(puzzle_input[card_index])):
            cards[card_index + i + 1] += count

    print(f"Part 2: {sum(cards.values())}")


if __name__ == "__main__":
    main()
