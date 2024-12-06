import sys
from utils import Point2D as Point
import enum


class Directions(enum.Enum):
    UP = Point(0, -1)
    RIGHT = Point(1, 0)
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)


class Loop(Exception):
    pass


class Grid:
    moves = {
        Directions.UP: Directions.RIGHT,
        Directions.RIGHT: Directions.DOWN,
        Directions.DOWN: Directions.LEFT,
        Directions.LEFT: Directions.UP,
    }
    dir_to_char = {Directions.UP: "^", Directions.RIGHT: ">", Directions.DOWN: "v", Directions.LEFT: "<"}

    def __init__(self, lines):
        self.grid = {}
        self.walls = set()
        self.height = len(lines)
        self.width = len(lines[0])
        self.guard = None
        self.guard_direction = Directions.UP
        self.path = set()

        for y, row in enumerate(lines):
            for x, char in enumerate(row):
                p = Point(x, y)
                if char == "^":
                    self.guard = p
                    char = "."

                self.grid[p] = char

                if char == "#":
                    self.walls.add(p)

    def walk(self, extra_wall=None):
        guard, guard_direction = self.guard, self.guard_direction
        path = {(guard, guard_direction)}

        while True:
            next_pos = guard + guard_direction.value

            if next_pos not in self.grid:
                # We're done
                break

            if (next_pos, guard_direction) in path:
                raise Loop

            if next_pos in self.walls or next_pos == extra_wall:
                guard_direction = self.moves[guard_direction]
                if (guard, guard_direction) in path:
                    raise Loop
                continue

            path.add((next_pos, guard_direction))
            guard = next_pos

        return {pos for pos, direction in path}


with open(sys.argv[1], "r") as file:
    grid = Grid([line.strip() for line in file])

path = grid.walk()
print(len(path))

loopers = 0
for p in path:
    try:
        length = grid.walk(p)
    except Loop:
        loopers += 1

print(loopers)