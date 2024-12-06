import sys
import enum


class Directions(enum.Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


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
                p = (x, y)
                if char == "^":
                    self.guard = p
                    char = "."

                self.grid[p] = char

                if char == "#":
                    self.walls.add(p)

    def walk(self, extra_wall=None):
        guard, guard_direction = self.guard, self.guard_direction
        path = {(guard, guard_direction)}
        points = {guard}

        while True:
            next_pos = (guard[0] + guard_direction.value[0], guard[1] + guard_direction.value[1])

            if next_pos not in self.grid:
                # We're done
                break

            if (next_pos, guard_direction) in path:
                raise Loop

            if next_pos in self.walls or next_pos == extra_wall:
                guard_direction = self.moves[guard_direction]
                if (guard, guard_direction) in path:
                    raise Loop
                path.add((guard, guard_direction))
                continue

            if extra_wall is None:
                points.add(next_pos)
            guard = next_pos

        return points


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
