import sys


class Board:
    width = 5
    match = (1 << width) - 1

    def __init__(self, lines):
        self.reset()
        self.numbers = {}

        for row, line in enumerate(lines):
            for col, n in enumerate(int(n.strip()) for n in line.split()):
                self.numbers[n] = (row, col)

    def reset(self):
        self.rows = [0 for i in range(Board.width)]
        self.cols = [0 for i in range(Board.width)]
        self.marked = set()
        self.won = False

    def mark(self, number):
        if self.won:
            # we only win once
            return False
        try:
            row, col = self.numbers[number]
        except KeyError:
            return False

        self.marked.add(number)
        self.rows[row] |= 1 << col
        self.cols[col] |= 1 << row

        self.won = self.match in (self.rows[row], self.cols[col])
        return self.won

    def score(self, mult):
        return mult * sum(self.numbers.keys() - self.marked)


with open(sys.argv[1], "r") as file:
    lines = [line.strip() for line in file.readlines()]

drawn = [int(number) for number in lines.pop(0).split(",")]


boards = [
    Board(lines[1 + i * (Board.width + 1) : (i + 1) * (Board.width + 1)])
    for i in range(len(lines) // (Board.width + 1))
]


def part_one():
    for number in drawn:
        for board_num, board in enumerate(boards):
            if board.mark(number):
                score = board.score(number)
                print(f"Board {board_num} wins with {number}, {score=}!")

                return score


def part_two():
    last_score = 0
    for number in drawn:
        for board_num, board in enumerate(boards):
            if board.mark(number):
                last_score = board.score(number)
                print(f"Board {board_num} wins with {number}, {last_score=}!")

    return last_score


print(part_one())

for board in boards:
    board.reset()

print(part_two())
