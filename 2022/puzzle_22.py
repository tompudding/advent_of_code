import sys


class Facing:
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


def get_num(path):
    pos = 0
    while pos < len(path) and path[pos] in "0123456789":
        pos += 1
    return path[pos:], int(path[:pos])


class Grid:
    def __init__(self, lines):
        self.height = len(lines)
        self.width = max((len(line) for line in lines))
        self.grid = {}
        self.neighbours = {}
        self.start = None

        for row, line in enumerate(lines):
            first_col = last_col = None
            for col, char in enumerate(line):
                if char == " ":
                    continue

                if self.start is None:
                    self.start = (col, row)

                self.grid[(col, row)] = char
                self.neighbours[col, row] = {}
                if first_col is None:
                    first_col = col
                else:
                    self.neighbours[(col, row)][Facing.LEFT] = (col - 1, row)
                last_col = col
                self.neighbours[(col, row)][Facing.RIGHT] = (col + 1, row)
            self.neighbours[(last_col, row)][Facing.RIGHT] = (first_col, row)
            self.neighbours[(first_col, row)][Facing.LEFT] = (last_col, row)

        for col in range(self.width):
            first_row = last_row = None
            for row in range(self.height):
                if (col, row) not in self.grid:
                    continue
                if first_row is None:
                    first_row = row
                else:
                    self.neighbours[(col, row)][Facing.UP] = (col, row - 1)
                last_row = row

                self.neighbours[(col, row)][Facing.DOWN] = (col, row + 1)
            self.neighbours[(col, last_row)][Facing.DOWN] = (col, first_row)
            self.neighbours[(col, first_row)][Facing.UP] = (col, last_row)

    def move(self, num):
        for i in range(num):
            next = self.neighbours[self.pos][self.facing]
            if self.grid[next] == "#":
                return
            self.pos = next

    def follow(self, path):
        self.facing = 0
        self.pos = self.start
        while path:
            path, num = get_num(path)
            self.move(num)
            if not path:
                break

            dir = path[0]
            if dir == "L":
                self.facing = (self.facing + 3) % 4
            elif dir == "R":
                self.facing = (self.facing + 1) % 4

            path = path[1:]


grid_lines = []
with open(sys.argv[1], "r") as file:
    for line in file:
        line = line.strip("\n")

        if not line:
            break
        grid_lines.append(line)

    for line in file:
        instructions = line.strip()

grid = Grid(grid_lines)

grid.follow(instructions)
print(1000 * (grid.pos[1] + 1) + 4 * (grid.pos[0] + 1) + grid.facing)
