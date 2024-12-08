import sys
from utils import Point2D as Point
import collections
import itertools


class Grid:
    def __init__(self, lines):
        self.grid = {}
        self.antennae = collections.defaultdict(list)
        self.height = len(lines)
        self.width = len(lines[0])

        for y, row in enumerate(lines):
            for x, char in enumerate(row):
                p = Point(x, y)
                self.grid[p] = char
                if char != ".":
                    self.antennae[char].append(p)

    def count_antinodes(self):
        antinodes = set()
        for name, antennae in self.antennae.items():
            for a, b in itertools.combinations(antennae, 2):
                diff = a - b
                # print(a, b, a + diff, b - diff)
                antinodes |= {antinode for antinode in (a + diff, b - diff) if antinode in self.grid}

        return len(antinodes)

    def count_resonant_antinodes(self):
        antinodes = set()
        for name, antennae in self.antennae.items():
            for a, b in itertools.combinations(antennae, 2):
                diff = a - b

                pos = a
                while pos in self.grid:
                    antinodes.add(pos)
                    pos += diff

                pos = b
                while pos in self.grid:
                    antinodes.add(pos)
                    pos -= diff

        return len(antinodes)


with open(sys.argv[1], "r") as file:
    grid = Grid([line.strip() for line in file])

print(grid.count_antinodes())
print(grid.count_resonant_antinodes())
