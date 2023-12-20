import sys
from utils import Point2D as Point


class Directions:
    NORTH = Point(0, -1)
    NORTH_EAST = Point(1, -1)
    EAST = Point(1, 0)
    SOUTH_EAST = Point(1, 1)
    SOUTH = Point(0, 1)
    SOUTH_WEST = Point(-1, 1)
    WEST = Point(-1, 0)
    NORTH_WEST = Point(-1, -1)

    all = {NORTH, NORTH_EAST, EAST, SOUTH_EAST, SOUTH, SOUTH_WEST, WEST, NORTH_WEST}

    def __init__(self):
        self.current = [
            [self.NORTH, self.NORTH_EAST, self.NORTH_WEST],
            [self.SOUTH, self.SOUTH_EAST, self.SOUTH_WEST],
            [self.WEST, self.NORTH_WEST, self.SOUTH_WEST],
            [self.EAST, self.NORTH_EAST, self.SOUTH_EAST],
        ]

    def step(self):
        self.current.append(self.current.pop(0))


class Grid:
    def __init__(self):
        self.grid = {}
        self.top_left = Point(0, 0)
        self.bottom_right = Point(0, 0)

    def add(self, elf):
        # if elf.pos.x < self.top_left.x:
        #     self.top_left.x = elf.pos.x
        # if elf.pos.y < self.top_left.y:
        #     self.top_left.y = elf.pos.y

        # if elf.pos.x > self.bottom_right.x:
        #     self.bottom_right.x = elf.pos.x
        # if elf.pos.y > self.bottom_right.y:
        #     self.bottom_right.y = elf.pos.y
        self.grid[elf.pos] = elf

    def remove(self, elf):
        # TODO: Contracting is more difficult. Maybe we don't need to?
        del self.grid[elf.pos]

    def bounds(self):
        top_left = Point(min(p.x for p in self.grid), min(p.y for p in self.grid))
        bottom_right = Point(max(p.x for p in self.grid), max(p.y for p in self.grid))
        return top_left, bottom_right

    def count(self):
        top_left, bottom_right = self.bounds()
        size = bottom_right - top_left
        return ((size.x + 1) * (size.y + 1)) - len(self.grid)

    def __contains__(self, pos):
        return pos in self.grid

    def __repr__(self):
        # This is inefficient in time but quite efficient in typing:
        top_left, bottom_right = self.bounds()

        out = ["-" * 80]

        for row in range(top_left.y, bottom_right.y + 1):
            line = []
            for col in range(top_left.x, bottom_right.x + 1):
                if Point(col, row) in self.grid:
                    line.append("#")
                else:
                    line.append(".")
            out.append("".join(line))
        return "\n".join(out)


grid = Grid()
elves = []


class Elf:
    def __init__(self, pos):
        self.pos = Point(*pos)

    def propose(self, directions):
        occupied = {dir: self.pos + dir in grid for dir in directions.all}
        if not any(occupied.values()):
            return None
        for dir_list in directions.current:
            if any(occupied[dir] for dir in dir_list):
                continue
            return self.pos + dir_list[0]

    def move_to(self, pos):
        grid.remove(self)
        self.pos = pos
        grid.add(self)


def round(elves, directions):
    proposals = {}
    for elf in elves:
        target = elf.propose(directions)
        if target is None:
            continue
        if target not in proposals:
            proposals[target] = elf
        else:
            proposals[target] = None

    num_moves = 0
    for target, elf in proposals.items():
        if elf is None:
            continue
        elf.move_to(target)
        num_moves += 1

    directions.step()
    # print(grid)
    return num_moves > 0


with open(sys.argv[1], "r") as file:
    for row, line in enumerate(file):
        line = line.strip()
        for col, char in enumerate(line):
            if char == "#":
                elf = Elf((col, row))
                elves.append(elf)
                grid.add(elf)
                # grid[elf.pos] = elf


directions = Directions()
# print(grid)

for count in range(10):
    round(elves, directions)
print(grid.count())


moved = True
while moved:
    moved = round(elves, directions)
    count += 1
print(count + 1)
