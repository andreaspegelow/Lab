from pathlib import Path
import copy


def parse_input(path: str):
    boards = []
    input = [i for i in Path(path).read_text().split("\n\n")]
    numbers = [int(i) for i in input[0].split(",")]

    for board in input[1:]:
        rows = board.split("\n")
        boards.append(
            [
                [int(number) for number in row.strip().replace("  ", " ").split(" ")]
                for row in rows
            ]
        )

    return (
        numbers,
        boards,
    )


def mark_number(number, boards):
    for board in boards:
        for row in board:
            for i, item in enumerate(row):
                if item == number:
                    row[i] = -1


def find_bingo(boards):
    winning_boards = []
    for board in boards:
        for row in board:
            if sum(row) == -5:
                # Winning row
                winning_boards.append(board)
                break
        for i in range(len(board)):
            column_count = 0
            for j in range(len(board)):
                column_count += board[j][i]
            if column_count == -5:
                # Winning column
                if board not in winning_boards:
                    winning_boards.append(board)
                break
    return winning_boards


def sum_winning_board(board):
    sum = 0
    for row in board:
        for number in row:
            if number != -1:
                sum += number
    return sum


def main():
    numbers, boards = parse_input("advent_of_code/2021/advent_of_code_day4/input.txt")
    for number in numbers:
        mark_number(number, boards)
        winning_boards = find_bingo(boards)
        if winning_boards:
            winning_sum = sum_winning_board(winning_boards[0])
            print(winning_sum * number)
            break

    numbers, boards = parse_input("advent_of_code/2021/advent_of_code_day4/input.txt")
    last_winnings = None
    for number in numbers:
        winning_boards = None
        mark_number(number, boards)
        winning_boards = find_bingo(boards)
        if winning_boards:
            last_winnings = (winning_boards, number)
            for board in winning_boards:
                boards.remove(board)

    winning_sum = sum_winning_board(last_winnings[0][0])
    print(winning_sum * last_winnings[1])


if __name__ == "__main__":
    main()
