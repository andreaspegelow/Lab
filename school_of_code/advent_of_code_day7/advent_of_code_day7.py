import re
from pathlib import Path


def find_parent_bags_to_bag(child_bag, rules):
    found_parent_bags = set()
    for rule in rules:
        parent_bag, rule = rule.split("contain")
        if re.search(child_bag, rule):
            parent_bag = parent_bag.strip().replace("bags", "")
            found_parent_bags.add(parent_bag)
            found_parent_bags.update(find_parent_bags_to_bag(parent_bag, rules))
    return found_parent_bags


def count_required_child_bags_for_bag(parent_bag, rules):
    count = 0
    for rule in rules:
        child_bag, rule = rule.split("contain")
        if re.search(parent_bag, child_bag):
            if rule != " no other bags.":
                childs = rule.split(",")
                for child in childs:
                    child = child.strip().replace(".", "").replace("bags", "")
                    count += int(child[:1])
                    count += int(child[:1]) * count_required_child_bags_for_bag(
                        child[2:], rules
                    )
    return count


def main():

    rules = Path("school_of_code/advent_of_code_day7/input_small.txt").read_text().split("\n")

    print(f"Part 1: {len(find_parent_bags_to_bag('shiny gold bag', rules))}")
    print(f"Part 2: {count_required_child_bags_for_bag('shiny gold bag', rules)}")


if __name__ == "__main__":
    main()
