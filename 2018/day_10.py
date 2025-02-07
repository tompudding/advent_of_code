import sys
import math
from collections import defaultdict
import enum
import re


class Directions(enum.Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    UP_RIGHT = (1, -1)
    DOWN_RIGHT = (1, 1)
    DOWN_LEFT = (-1, 1)
    UP_LEFT = (-1, -1)


class Star:
    def __init__(self, data):
        groups = re.match("position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>", data).groups()
        self.pos = tuple([int(v) for v in groups[:2]])
        self.vel = tuple([int(v) for v in groups[2:]])
        self.start_pos = tuple(self.pos)

    def step(self, n):
        self.pos = ((self.pos[0] + self.vel[0] * n), (self.pos[1] + self.vel[1] * n))

    def reset(self):
        self.pos = self.start_pos


def draw(stars):
    x_bounds = [min(star.pos[0] for star in stars), max(star.pos[0] for star in stars) + 1]
    y_bounds = [min(star.pos[1] for star in stars), max(star.pos[1] for star in stars) + 1]
    positions = {star.pos for star in stars}

    for y in range(*y_bounds):
        line = []
        for x in range(*x_bounds):
            line.append("*" if (x, y) in positions else " ")
        print("".join(line))


def step(stars):
    for star in stars:
        star.step(1)


def all_adjacent(stars):
    positions = {star.pos for star in stars}

    for star in stars:
        if all(
            (
                (star.pos[0] + direction.value[0], star.pos[1] + direction.value[1]) not in positions
                for direction in Directions
            )
        ):
            return False

    return True


with open(sys.argv[1], "r") as file:
    stars = [Star(line) for line in file]


for star in stars:
    star.reset()

heat_map = defaultdict(int)

best_solo = 2 ** 20

for i in range(50000):
    if all_adjacent(stars):
        print("All Adjacent at seconds=", i)
        draw(stars)
        break
    step(stars)
