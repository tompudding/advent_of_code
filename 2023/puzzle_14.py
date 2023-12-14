import sys


class Grid:
    def __init__(self, lines):
        self.rows = [list(line) for line in lines]
        self.height = len(self.rows)
        self.width = len(self.rows[0])
        self.cols = [[row[i] for row in self.rows] for i in range(self.width)]
        self.positions = set()

        for y, row in enumerate(self.rows):
            for x, char in enumerate(row):
                if self.rows[x][y] == "O":
                    self.positions.add((x, y))

        self.positions = frozenset(self.positions)

    # Copy-paste!
    def up(self):
        total = 0

        for x, col in enumerate(self.cols):
            pos = 0
            for y, char in enumerate(col):
                if char == "O":
                    self.rows[y][x] = "."
                    self.rows[pos][x] = "O"
                    pos += 1
                elif char == "#":
                    pos = y + 1

        self.cols = [[row[i] for row in self.rows] for i in range(self.width)]

    def down(self):
        total = 0

        for x, col in enumerate(self.cols):
            pos = self.height - 1
            for y in range(len(col) - 1, -1, -1):
                char = col[y]
                if char == "O":
                    self.rows[y][x] = "."
                    self.rows[pos][x] = "O"
                    pos -= 1
                elif char == "#":
                    pos = y - 1

        self.cols = [[row[i] for row in self.rows] for i in range(self.width)]

    def left(self):
        for y, row in enumerate(self.rows):
            pos = 0
            for x, char in enumerate(row):
                if char == "O":
                    self.cols[x][y] = "."
                    self.cols[pos][y] = "O"
                    pos += 1
                elif char == "#":
                    pos = x + 1

        self.rows = [[col[i] for col in self.cols] for i in range(self.height)]

    def right(self):
        self.positions = set()
        for y, row in enumerate(self.rows):
            pos = self.width - 1
            for x in range(len(row) - 1, -1, -1):
                char = row[x]
                if char == "O":
                    self.cols[x][y] = "."
                    self.cols[pos][y] = "O"
                    self.positions.add((pos, y))
                    pos -= 1
                elif char == "#":
                    pos = x - 1
        self.positions = frozenset(self.positions)

        self.rows = [[col[i] for col in self.cols] for i in range(self.height)]

    def cycle(self):
        self.up()
        self.left()
        self.down()
        self.right()

    def load(self):
        total = 0
        for y, row in enumerate(self.rows):
            for x, char in enumerate(row):
                if char == "O":
                    total += self.height - y

        return total

    def __repr__(self):
        out = []

        for row in self.rows:
            out.append("".join(row))
        return "\n".join(out)


with open(sys.argv[1], "r") as file:
    lines = [line.strip() for line in file if line]

grid = Grid(lines)

grid.up()
print(grid.load())


grid = Grid(lines)

path = {grid.positions: 0}
path_by_count = {}
count = 0

while True:
    grid.cycle()
    count += 1

    if grid.positions in path:
        meet_point = path[grid.positions]
        cycle_length = count - meet_point
        print(path_by_count[meet_point + ((1000000000 - meet_point) % cycle_length)])
        break

    path[grid.positions] = count
    path_by_count[count] = grid.load()
