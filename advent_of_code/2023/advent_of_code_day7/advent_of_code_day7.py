from pathlib import Path
from typing import List

rankings1 = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
rankings2 = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]


def parse_input(path: str) -> List[int]:
    return [(i.split()[0], i.split()[1]) for i in Path(path).read_text().split("\n")]


def hand_value(hand, rankings):
    value = ""
    for card in hand:
        value += str(10 + rankings.index(card))
    return value


def hand_type(hand, rankings, joker=False):
    original_hand = hand
    
    if hand == "JJJJJ":
        hand = "AAAAA"
        
    if joker and "J" in hand:
        temp = set(hand)
        temp.remove("J")

        replace_with = ""
        max_count = 0
        for current_car in temp:
            current_count = hand.count(current_car)
            if current_count > max_count:
                max_count = current_count
                replace_with = current_car
            elif current_count == max_count:
                if int(hand_value(current_car, rankings)) > int(
                    hand_value(replace_with, rankings)
                ):
                    replace_with = current_car

        hand = hand.replace("J", replace_with)

    if len(set(hand)) == 1:
        return "7" + hand_value(original_hand, rankings)
    elif len(set(hand)) == 2:
        if hand.count(list(set(hand))[0]) in [1, 4]:
            return "6" + hand_value(original_hand, rankings)
        return "5" + hand_value(original_hand, rankings)
    elif len(set(hand)) == 3:
        if max(hand.count(x) for x in set(hand)) == 3:
            return "4" + hand_value(original_hand, rankings)
        return "3" + hand_value(original_hand, rankings)
    elif len(set(hand)) == 4:
        return "2" + hand_value(original_hand, rankings)
    elif len(set(hand)) == 5:
        for rank in reversed(rankings):
            if rank in hand:
                return "1" + hand_value(original_hand, rankings)


def main():
    hands = parse_input("advent_of_code/2023/advent_of_code_day7/input.txt")
    # hands = parse_input("advent_of_code/2023/advent_of_code_day7/input_small.txt")

    hands = sorted(hands, key=lambda hand: int(hand_type(hand[0], rankings1)))
    result = sum(i * int(hand[1]) for i, hand in enumerate(hands, start=1))
    print(f"Part 1: {result}")

    hands = parse_input("advent_of_code/2023/advent_of_code_day7/input.txt")
    # hands = parse_input("advent_of_code/2023/advent_of_code_day7/input_small.txt")

    hands = sorted(hands, key=lambda hand: int(hand_type(hand[0], rankings2, True)))
    result = sum(i * int(hand[1]) for i, hand in enumerate(hands, start=1))
    print(f"Part 2: {result}")


if __name__ == "__main__":
    main()
