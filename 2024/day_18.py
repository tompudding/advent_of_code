import sys
from dataclasses import dataclass
from utils import Point2D as Point
import heapq
import enum


class NoPath(Exception):
    pass


class Directions(enum.Enum):
    UP = Point(0, -1)
    RIGHT = Point(1, 0)
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


class Grid:
    moves = (Directions.UP, Directions.LEFT, Directions.RIGHT, Directions.DOWN)

    def __init__(self, lines):
        self.grid = {}
        self.walls = set()

        self.height = 71 if len(lines) > 100 else 7
        self.width = self.height
        self.walls = []
        self.wall_subset = set()
        self.start = (0, 0)
        self.end = (self.width - 1, self.height - 1)
        self.path = set()

        for line in lines:
            x, y = (int(v) for v in line.strip().split(","))
            self.walls.append((x, y))

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbours_part_one(self, walls, pos):

        for direction in Directions:
            next_pos = add(pos, direction.value)

            if next_pos in walls:
                continue

            if not ((0 <= next_pos[0] < self.width) and 0 <= next_pos[1] < self.height):
                continue

            yield next_pos, 1

    def find_path(self, num_walls):

        walls = {self.walls[i] for i in range(num_walls)}

        frontier = []
        start = self.start
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while frontier:
            s, pos = heapq.heappop(frontier)

            if pos == self.end:
                # Got it!
                break

            for next_pos, cost in self.get_neighbours_part_one(walls, pos):
                new_cost = cost_so_far[pos] + cost

                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + self.heuristic(pos, next_pos)
                    heapq.heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = pos

        else:
            raise NoPath()

        return cost_so_far[self.end]

    def __repr__(self):
        out = []
        for y in range(self.height):
            line = []
            for x in range(self.width):
                if (x, y) in self.wall_subset:
                    char = "#"
                elif (x, y) in self.path:
                    char = "O"
                else:
                    char = "."
                line.append(char)
            out.append("".join(line))
        return "\n".join(out)


with open(sys.argv[1], "r") as file:
    grid = Grid([line.strip() for line in file])


part_one_walls = 1024 if grid.width == 71 else 12
print(grid.find_path(part_one_walls))


# For part 2 can we binary search the right place?
low = part_one_walls
high = len(grid.walls)

while True:
    mid = low + ((high - low) // 2)

    try:
        cost = grid.find_path(mid)
        good = True
    except NoPath:
        good = False

    # print(f"tested {mid} {good=} {low=} {high=}")
    if good:
        low = mid
    else:
        high = mid

    if low + 1 == high:
        break

print(",".join([str(v) for v in grid.walls[low]]))
