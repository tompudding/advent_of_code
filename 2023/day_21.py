import sys


class Directions:
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

    adjacent = {UP, RIGHT, DOWN, LEFT}
    horizontal = {LEFT, RIGHT}
    vertical = {UP, DOWN}

    char = {UP: "^", RIGHT: ">", LEFT: "<", DOWN: "v"}


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


class Grid:
    def __init__(self, lines):
        self.height = len(lines)
        self.width = len(lines[0])
        self.walls = set()

        for y, row in enumerate(lines):
            for x, char in enumerate(row):
                if char == "#":
                    self.walls.add((x, y))
                elif char == "S":
                    self.start = (x, y)

        self.walk_positions = {self.start}

    def step(self, n):
        for i in range(n):
            new_positions = set()

            for pos in self.walk_positions:
                new_positions |= {add(pos, off) for off in Directions.adjacent} - self.walls

            self.walk_positions = new_positions

    def __repr__(self):
        out = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if (x, y) in self.walls:
                    char = "#"
                elif (x, y) in self.walk_positions:
                    char = "O"
                else:
                    char = "."

                row.append(char)

            out.append("".join(row))

        return "\n".join(out)


with open(sys.argv[1], "r") as file:
    grid = Grid([line.strip() for line in file])

grid.step(64)
print(grid)
print(len(grid.walk_positions))
