import sys
from dataclasses import dataclass
from utils import Point2D as Point
from collections import defaultdict
import heapq
import enum


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
        self.spaces = set()

        self.height = len(lines)
        self.width = len(lines[0])
        self.keys = {}
        self.doors = {}
        self.pos = None
        self.inner_portals = {}
        self.outer_portals = {}
        self.neighbours = defaultdict(list)
        self.wall_range = [[self.width, 0], [self.height, 0]]

        # For debugging, the locations of the named portals
        self.ipn = {}
        self.opn = {}
        self.portal_names = {}

        portals = defaultdict(list)

        for y, row in enumerate(lines):
            for x, char in enumerate(row):
                p = Point(x, y)
                # self.grid[p] = char
                if char == "#":
                    self.walls.add(p)
                    if p.x < self.wall_range[0][0]:
                        self.wall_range[0][0] = p.x
                    if p.y < self.wall_range[1][0]:
                        self.wall_range[1][0] = p.y
                    if p.x > self.wall_range[0][1]:
                        self.wall_range[0][1] = p.x
                    if p.y > self.wall_range[1][1]:
                        self.wall_range[1][1] = p.y
                    self.grid[p] = "#"
                elif char == ".":
                    self.spaces.add(p)

                elif char.isupper():
                    # Is this a horizontal or vertical name?
                    name = [char]
                    for direction in Directions.RIGHT, Directions.DOWN:
                        l = p + direction.value
                        try:
                            c = lines[l[1]][l[0]]
                        except IndexError:
                            continue
                        if c.isupper():
                            name.append(c)
                            pos = l
                            break
                    else:
                        continue
                    name = "".join(name)
                    portals[name].append((pos, direction))

        def get_portal_neighbour(p, direction):
            # Either p + direction or p - 2*direction should be in spaces, that's the point that we're really
            # interested in
            for diff in direction.value, direction.value * -2:
                x = p + diff
                if x in self.spaces:
                    return x
            raise NoJawn()

        self.start = get_portal_neighbour(*portals["AA"][0])
        self.end = get_portal_neighbour(*portals["ZZ"][0])
        del portals["AA"]
        del portals["ZZ"]

        for name, (a, b) in portals.items():
            A, B = (get_portal_neighbour(*x) for x in (a, b))

            # We want A to be the inner portal
            if self.is_interior(b[0]):
                A, B = B, A

            self.inner_portals[A] = B
            self.outer_portals[B] = A

            self.ipn[name] = A
            self.opn[name] = B

        for name, p in self.ipn.items():
            self.portal_names[p] = f"{name}(inner)"
        for name, p in self.opn.items():
            self.portal_names[p] = f"{name}(outer)"

        self.compress_graph()

    def is_interior(self, pos):
        # If one of it's
        return (
            self.wall_range[0][0] < pos.x < self.wall_range[0][1]
            and self.wall_range[1][0] < pos.y < self.wall_range[1][1]
        )

    def heuristic(self, pos, level):
        # Try just use how many keys we have left
        return abs(pos[0] - self.end[0]) + abs(pos[1] - self.end[1]) + (level * 20)

    def get_neighbours_basic(self, pos):
        for direction in Directions:
            next_pos = pos + direction.value

            if next_pos in self.spaces:
                yield next_pos, 0

        if pos in self.inner_portals:
            yield self.inner_portals[pos], 1

        if pos in self.outer_portals:
            yield self.outer_portals[pos], -1

    def compress_graph(self):
        # first get all the points with 3 paths
        nodes = {self.start, self.end} | {p for p in self.inner_portals} | {p for p in self.outer_portals}
        for p in self.spaces:
            neighbours = [n[0] for n in self.get_neighbours_basic(p)]
            if len(neighbours) >= 3:
                nodes.add(p)

        # Now we add the directions for each of those nodes.

        for node in nodes:
            # For each of the neighbours of this node, we walk in that direction until we reach another node
            for neighbour, level_change in self.get_neighbours_basic(node):
                last = node
                pos = neighbour
                cost = 1
                while pos not in nodes:
                    next_positions = {n[0] for n in self.get_neighbours_basic(pos)} - {last}
                    if len(next_positions) == 0:
                        # dead end
                        break
                    assert len(next_positions) == 1
                    last = pos
                    pos = next_positions.pop()
                    cost += 1
                else:
                    self.neighbours[node].append((pos, cost, level_change))

    def get_neighbours(self, pos, level, scale_factor):

        for target, cost, level_change in self.neighbours[pos]:
            new_level = level + level_change * scale_factor
            if new_level < 0:
                continue

            yield target, cost, new_level

    def find_path(self, scale_factor):
        frontier = []
        start = (grid.start, 0)
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        target = (grid.end, 0)

        while frontier:
            s, (pos, level) = heapq.heappop(frontier)

            if (pos, level) == target:
                # Got it!
                break

            for next_pos, cost, new_level in grid.get_neighbours(pos, level, scale_factor):
                new_state = (next_pos, new_level)
                new_cost = cost_so_far[(pos, level)] + cost

                if new_state not in cost_so_far or new_cost < cost_so_far[new_state]:
                    cost_so_far[new_state] = new_cost
                    priority = new_cost + grid.heuristic(*new_state)
                    heapq.heappush(frontier, (priority, new_state))
                    came_from[new_state] = pos, level

        else:
            print("Failed to find the path")
            raise Bad()

        return cost_so_far[target]


with open(sys.argv[1], "r") as file:
    grid = Grid([line.strip("\n") for line in file])

print(grid.find_path(scale_factor=0))
print(grid.find_path(scale_factor=1))
