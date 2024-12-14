import sys
import math
from collections import defaultdict
import enum

WIDTH = 101
HEIGHT = 103


class Directions(enum.Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    UP_RIGHT = (1, -1)
    DOWN_RIGHT = (1, 1)
    DOWN_LEFT = (-1, 1)
    UP_LEFT = (-1, -1)


class Robot:
    def __init__(self, data):
        parts = data.strip().split()
        self.pos = tuple([int(v.strip()) for v in parts[0].split("p=")[1].split(",")])
        self.vel = tuple([int(v.strip()) for v in parts[1].split("v=")[1].split(",")])
        self.start_pos = tuple(self.pos)

    def step(self, n):
        self.pos = ((self.pos[0] + self.vel[0] * n) % WIDTH, (self.pos[1] + self.vel[1] * n) % HEIGHT)

    def reset(self):
        self.pos = self.start_pos

    def walk(self):
        self.reset()
        yield self.pos
        self.step(1)

        while self.pos != self.start_pos:
            yield self.pos
            self.step(1)


def score(robots):
    quadrants = [0, 0, 0, 0]
    for robot in robots:
        robot.step(100)

        if robot.pos[0] == WIDTH // 2 or robot.pos[1] == HEIGHT // 2:
            # Middle so doesn't count
            continue

        left = robot.pos[0] < WIDTH // 2
        top = robot.pos[1] < HEIGHT // 2

        quadrants[left * 2 + top] += 1

    return math.prod(quadrants)


def draw(robots):
    positions = {robot.pos for robot in robots}
    for y in range(HEIGHT // 2):
        line = []
        for x in range(WIDTH):
            line.append("*" if (x, y) in positions else " ")
        print("".join(line))


def step(robots):
    for robot in robots:
        robot.step(1)


def count_solo(robots):
    positions = {robot.pos for robot in robots}
    count = 0
    for robot in robots:
        if any(
            (
                (robot.pos[0] + direction.value[0], robot.pos[1] + direction.value[1]) in positions
                for direction in Directions
            )
        ):
            continue
        count += 1

    return count


with open(sys.argv[1], "r") as file:
    robots = [Robot(line) for line in file]

print(score(robots))

for robot in robots:
    robot.reset()

heat_map = defaultdict(int)

best_solo = WIDTH * HEIGHT

for i in range(WIDTH * HEIGHT):
    # draw(robots)
    solo = count_solo(robots)
    if solo < best_solo:
        print("New best solo", solo, i)
        best_solo = solo
        draw(robots)
    step(robots)
    # print(i)
