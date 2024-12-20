import sys
from dataclasses import dataclass
from collections import defaultdict
from utils import Point2D as Point
import heapq
import enum


class Directions(enum.Enum):
    UP = Point(0, -1)
    RIGHT = Point(1, 0)
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def manhattan(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


class Grid:
    def __init__(self, lines):
        self.grid = {}
        self.walls = set()

        self.height = len(lines)
        self.width = len(lines[0])
        self.walls = set()
        self.start = None
        self.end = None
        self.path = {}
        self.spaces = set()

        for y, row in enumerate(lines):
            for x, char in enumerate(row):
                p = (x, y)
                self.grid[p] = char
                if char == ".":
                    self.spaces.add(p)
                elif char == "#":
                    self.walls.add(p)
                elif char == "S":
                    self.start = p
                elif char == "E":
                    self.end = p
                    self.spaces.add(p)

        # Now we build the path
        pos = self.start
        step = 0
        self.path[pos] = step
        while pos != self.end:
            for direction in Directions:
                next_pos = add(pos, direction.value)

                if next_pos in self.spaces and next_pos not in self.path:
                    break
            else:
                raise BadPath()

            step += 1
            pos = next_pos
            self.path[pos] = step

    def find_shortcuts(self):
        # For every step of the path, we try all two step combos and see if they put us somewhere better
        count = 0

        for pos, step in self.path.items():
            for i in Directions:
                for j in Directions:
                    step_one = add(pos, i.value)
                    step_two = add(step_one, j.value)

                    best = step
                    if step_two in self.path:
                        best = min(best, self.path[step_two] + 2)

                    if best < step and step_one in self.walls and step - best >= 100:
                        count += 1

        return count

    def find_bigshortcuts(self):
        # For every step of the path, we'll look backwards from the other end to see if we can jump to it in
        # 20 moves or fewer
        count = 0

        for pos, step in self.path.items():
            for target, target_step in reversed(self.path.items()):
                if target == pos:
                    break
                diff = manhattan(pos, target)
                if diff > 20:
                    continue
                saving = target_step - diff - step
                if saving >= 100:
                    count += 1
        return count


with open(sys.argv[1], "r") as file:
    grid = Grid([line.strip() for line in file])

print(grid.find_shortcuts())
print(grid.find_bigshortcuts())
