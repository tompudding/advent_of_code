import sys
import enum


class Directions:
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

    adjacent = {UP, RIGHT, DOWN, LEFT}


def add(pos, other):
    return (pos[0] + other[0], pos[1] + other[1])


class Pipe:
    translate = {"L": "└", "F": "┌", "J": "┘", "7": "┐", "|": "│", "-": "─", ".": " "}

    connects = {
        "│": {Directions.UP, Directions.DOWN},
        "─": {Directions.LEFT, Directions.RIGHT},
        "└": {Directions.UP, Directions.RIGHT},
        "┌": {Directions.DOWN, Directions.RIGHT},
        "┘": {Directions.LEFT, Directions.UP},
        "┐": {Directions.LEFT, Directions.DOWN},
        " ": set(),
    }

    bolden = {
        "│": "┃",
        "─": "━",
        "└": "┗",
        "┌": "┏",
        "┘": "┛",
        "┐": "┓",
    }

    def __init__(self, pos, char):
        try:
            char = self.translate[char]
        except KeyError:
            pass

        self.char = char
        self.pos = pos
        self.is_loop = False
        self.is_exterior = False
        try:
            self.bold = self.bolden[char]
        except KeyError:
            self.bold = char

        if char != "S":
            self.connects_to = {add(self.pos, direction) for direction in self.connects[self.char]}
        else:
            # We have to work this out later
            self.connects_to = {}

    def __repr__(self):
        if self.is_loop:
            return self.bold

        if self.is_exterior:
            return "O"

        else:
            return "I"
        # return self.bold if self.is_bold else self.char


class Grid:
    def __init__(self, lines):
        self.connects_to = {}
        self.connects_from = {}
        self.grid = {}
        self.start = None

        self.rows = []

        for row, line in enumerate(lines):
            current_row = []
            for col, char in enumerate(line):
                pos = (col, row)
                pipe = Pipe(pos, char)
                current_row.append(pipe)
                if pipe.char == "S":
                    self.start = pos
                self.grid[col, row] = pipe

                try:
                    self.connects_from[col, row] |= pipe.connects_to
                except KeyError:
                    self.connects_from[col, row] = set(pipe.connects_to)

                for other in pipe.connects_to:
                    try:
                        self.connects_to[other].add(pos)
                    except KeyError:
                        self.connects_to[other] = {pos}
            self.rows.append(current_row)

        # Now we can find what the start is connected to and fill that in
        self.grid[self.start].connects_to = self.connects_to[self.start]
        self.grid[self.start].is_loop = True

        self.width = len(self.rows[0])
        self.height = len(self.rows)

        # Find the one loop
        self.loop = self.find_loop()
        self.loop_tiles = set(self.loop)

        self.exterior = self.find_exterior()

        for tile in self.exterior:
            self.grid[tile].is_exterior = True

    def get_neighbours(self, pos):
        # Start with this being simple
        new = {add(pos, diff) for diff in Directions.adjacent} - self.loop_tiles
        return {
            pos for pos in new if pos[0] >= 0 and pos[0] < self.width and pos[1] >= 0 and pos[1] < self.height
        }

    def find_exterior(self):
        # The frontier starts as all the edge tiles that aren't in the path

        frontier = (
            {(0, row) for row in range(self.height)}
            | {(col, 0) for col in range(self.width)}
            | {(self.width - 1, row) for row in range(self.height)}
            | {(col, self.height - 1) for col in range(self.width)}
        )

        frontier -= self.loop_tiles

        exterior = set(frontier)
        examined = set()

        while frontier:
            current = frontier.pop()
            examined.add(current)
            exterior.add(current)
            new = self.get_neighbours(current)
            exterior |= new

            frontier = exterior - examined

        return exterior

    def find_loop(self):
        # We start at the start, pick one of the directions, and then follow the path until we're back at the start
        steps = self.grid[self.start].connects_to
        assert len(steps) == 2
        pos = next(iter(steps))

        path = [self.start, pos]
        self.grid[pos].is_loop = True

        while pos != self.start:
            steps = self.grid[pos].connects_to - {path[-2]}
            assert len(steps) == 1
            pos = steps.pop()
            self.grid[pos].is_loop = True
            if pos == self.start:
                break
            path.append(pos)

        return path

    def find_furthest_point(self):
        return len(self.loop) // 2

    def __repr__(self):
        out = []
        for row in self.rows:
            out.append("".join((str(char) for char in row)))
        return "\n".join(out)


with open(sys.argv[1], "r") as file:
    lines = [line.strip() for line in file]

grid = Grid(lines)

print(grid)

print(grid.find_furthest_point())
