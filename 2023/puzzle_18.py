import sys
import itertools


class RightWall:
    char = "R"
    is_horizontal = True

    def __init__(self, length):
        self.length = length

    def generate(self, x, y):
        return (x + self.length, y)


class LeftWall(RightWall):
    char = "L"
    is_horizontal = True

    def generate(self, x, y):
        return (x - self.length, y)


class UpWall(RightWall):
    char = "U"
    is_horizontal = False

    def generate(self, x, y):
        return (x, y - self.length)


class DownWall(UpWall):
    char = "D"
    is_horizontal = False

    def generate(self, x, y):
        return (x, y + self.length)


def shoelace(vertices):
    return sum([(a[0] * b[1]) - (a[1] * b[0]) for a, b in itertools.pairwise(vertices)]) // 2


class Quarry:
    def __init__(self, walls):
        pos = (0, 0)

        self.walls = walls

        self.vertices = [pos]

        for wall in walls:
            pos = wall.generate(*pos)
            self.vertices.append(pos)

        self.area = shoelace(self.vertices)
        self.edge = sum(wall.length for wall in walls)
        self.capacity = (self.area + 1) - (self.edge // 2) + self.edge


wall_lookup = {wall.char: wall for wall in (RightWall, UpWall, DownWall, LeftWall)}

with open(sys.argv[1], "r") as file:
    part_one_walls = []
    part_two_walls = []
    for line in file:
        wall_type, length, colour = line.strip().split()
        part_one_walls.append(wall_lookup[wall_type](int(length)))

        data = int(colour.strip("()#"), 16)
        length = data >> 4
        wall_type = [RightWall, DownWall, LeftWall, UpWall][data & 0xF]
        part_two_walls.append(wall_type(int(length)))

quarry = Quarry(part_one_walls)
print(quarry.capacity)

quarry = Quarry(part_two_walls)
print(quarry.capacity)
