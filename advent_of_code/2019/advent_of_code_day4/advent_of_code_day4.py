def has_duplicated_digit(number: int, max_repeats=None) -> bool:
    s = str(number)
    if max_repeats:
        return any(s.count(digit) == max_repeats for digit in set(s))
    else:
        return len(s) != len(set(s))


def is_increasing(number: int) -> bool:
    s = list(str(number))
    return all(a <= b for a, b in zip(s, s[1:]))


def make_increasing(number: int) -> int:
    number_list = list(map(int, str(number)))
    for i in range(len(number_list) - 1):
        if number_list[i] > number_list[i + 1]:
            number_list[i + 1 :] = [number_list[i]] * len(number_list[i + 1 :])
            break
    return int("".join(map(str, number_list)))


def next_valid_password(number: int) -> str:
    number += 1
    new_number = make_increasing(number)
    if has_duplicated_digit(new_number, max_repeats=2):
        return new_number
    else:
        return next_valid_password(new_number)


def main():
    start = 236491
    end = 713787

    # collected = [i for i in range(start, end) if is_increasing(i) and has_duplicated_digit(i)]
    # print(f"Part 1: {len(collected)}")
    # collected = [i for i in range(start, end) if is_increasing(i) and has_duplicated_digit(i, max_repeats=2)]
    # print(f"Part 2: {len(collected)}")

    collected = []
    password = start
    while password < end:
        password = next_valid_password(password)
        collected.append(password)
    collected[:-1]
    print(f"Part 1: {len(collected)}")


if __name__ == "__main__":
    main()
