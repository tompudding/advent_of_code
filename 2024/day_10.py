import sys
import collections
import enum


class Directions(enum.Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


class Grid:
    START_ALTITUDE = 0
    END_ALTITUDE = 9

    def __init__(self, lines):
        self.grid = {}
        self.height = len(lines)
        self.width = len(lines[0])
        self.trailheads = set()

        for y, row in enumerate(lines):
            for x, alt in enumerate(row):
                p = (x, y)
                try:
                    alt = int(alt)
                except ValueError:
                    alt = -1
                self.grid[p] = alt
                if alt == self.START_ALTITUDE:
                    self.trailheads.add(p)

        self.neighbours = collections.defaultdict(set)
        # Create the neighbours
        for point, alt in self.grid.items():
            for direction in Directions:
                neighbour = (point[0] + direction.value[0], point[1] + direction.value[1])
                try:
                    other_alt = self.grid[neighbour]
                    if other_alt == alt + 1:
                        self.neighbours[point].add(neighbour)
                except KeyError:
                    continue

    def rate_trail(self, trailhead, rate=False):
        frontier = {trailhead}
        visited = set()

        count = 0
        reachable = set()
        came_from = collections.defaultdict(set)
        while frontier:
            pos = frontier.pop()
            visited.add(pos)

            for neighbour in self.neighbours[pos]:
                if self.grid[neighbour] == self.END_ALTITUDE:
                    reachable.add(neighbour)
                came_from[neighbour].add(pos)
                frontier.add(neighbour)

        if not rate:
            return len(reachable)

        # For rating we'll recursively count all the ways we can go back from each trailend

        def count(pos):
            if pos == trailhead:
                return 1

            total = 0
            for other_pos in came_from[pos]:
                total += count(other_pos)

            return total

        return sum(count(trailend) for trailend in reachable)

    def count_all_trails(self):
        return sum(self.rate_trail(trailhead, rate=False) for trailhead in self.trailheads)

    def rate_all_trails(self):
        return sum(self.rate_trail(trailhead, rate=True) for trailhead in self.trailheads)


with open(sys.argv[1], "r") as file:
    grid = Grid([line.strip() for line in file])

print(grid.count_all_trails())

print(grid.rate_all_trails())
