import sys
import collections
import enum


class Directions:
    UP = complex(0, -1)
    RIGHT = complex(1, 0)
    DOWN = complex(0, 1)
    LEFT = complex(-1, 0)

    adjacent = (
        UP,
        RIGHT,
        DOWN,
        LEFT,
        UP + RIGHT,
        UP + LEFT,
        DOWN + RIGHT,
        DOWN + LEFT,
    )


class Grid:
    def __init__(self, lines):
        self.grid = {}
        self.rolls = set()
        self.adjacent_counts = collections.defaultdict(int)
        self.height = len(lines)
        self.width = len(lines[0])
        self.trailheads = set()

        for y, row in enumerate(lines):
            for x, char in enumerate(row):
                p = complex(x, y)
                self.grid[p] = char
                if "@" == char:
                    self.rolls.add(p)
                    for direction in Directions.adjacent:
                        self.adjacent_counts[p + direction] += 1

    def get_nice_rolls(self):
        return [p for p in self.rolls if self.adjacent_counts[p] < 4]

    def remove_rolls(self, rolls):
        for p in rolls:
            self.rolls.remove(p)
            for direction in Directions.adjacent:
                self.adjacent_counts[p + direction] -= 1


with open(sys.argv[1], "r") as file:
    grid = Grid([line.strip() for line in file])

print(len(grid.get_nice_rolls()))

# for part 2 we want to keep removing those rolls
nice_rolls = grid.get_nice_rolls()
count = len(nice_rolls)
while nice_rolls:
    grid.remove_rolls(nice_rolls)
    nice_rolls = grid.get_nice_rolls()
    count += len(nice_rolls)

print(count)
