import sys


class Grid:
    def __init__(self, lines):
        self.height = len(lines)
        self.width = max((len(line) for line in lines))
        self.grid = {}
        self.neighbours = {}
        self.start = None

        for row, line in enumerate(lines):
            first = last = None
            for col, char in enumerate(line):
                if char == " ":
                    continue

                self.grid[(col, row)] = char
                if first is None:
                    first = col
                last = col


grid_lines = []
with open(sys.argv[1], "r") as file:
    for line in file:
        line = line.strip()

        if not line:
            break
        grid_lines.append(line)

    for line in file:
        instructions = line.strip()

grid = Grid(grid_lines)
