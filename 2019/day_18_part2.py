import sys
from dataclasses import dataclass
from utils import Point2D as Point
import heapq
import enum


class Directions(enum.Enum):
    UP = Point(0, -1)
    RIGHT = Point(1, 0)
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)
    UP_RIGHT = UP + RIGHT
    DOWN_RIGHT = DOWN + RIGHT
    DOWN_LEFT = DOWN + LEFT
    UP_LEFT = UP + LEFT


@dataclass
class Door:
    name: str

    def __str__(self):
        return self.name.upper()


@dataclass
class Key(Door):
    name: str
    pos: Point

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return other.name == self.name


class Grid:
    moves = (Directions.UP, Directions.LEFT, Directions.RIGHT, Directions.DOWN)

    def __init__(self, lines):
        self.grid = {}
        self.walls = set()

        self.height = len(lines)
        self.width = len(lines[0])
        self.keys = {}
        self.doors = {}
        self.pos = []

        if len(lines) >= 39:
            lines[39] = lines[39][:39] + "@#@" + lines[39][42:]
            lines[40] = lines[40][:39] + "###" + lines[40][42:]
            lines[41] = lines[41][:39] + "@#@" + lines[41][42:]

        for y, row in enumerate(lines):
            for x, char in enumerate(row):
                if char == ".":
                    continue
                p = Point(x, y)
                # self.grid[p] = char
                if char == "#":
                    self.walls.add(p)
                    self.grid[p] = "#"
                elif char.isupper():
                    door = Door(char.lower())
                    self.grid[p] = door
                    self.doors[p] = door
                elif char == "@":
                    self.pos.append(p)
                elif char.islower():
                    key = Key(char, p)
                    self.grid[p] = key
                    self.keys[p] = key

        self.pos = tuple(self.pos)
        self.compress_graph()

    def heuristic(self, pos, keys):
        # Try just use how many keys we have left
        return len(self.keys) - len(keys)

    def compress_graph(self):
        # We want the neighbour of each point (which is a position and a set of current keys) to be the keys
        # it can collect and the steps it takes to get there. To do that we'll do flood-fill algorithm from
        # each of the key positions (and the start position). This only works as there don't appear to be
        # cycles in the map.
        #
        # Note that this also doesn't work on the last two examples because they have to go back on themselves
        # with more keys, but it works on my input /shrug
        self.compressed = {}

        for current_start in self.pos:
            for start, key in (self.keys | {current_start: None}).items():
                frontier = {(start, 0, frozenset({key.name}) if key else frozenset(), frozenset())}
                visited = set()
                map_to = {}

                while frontier:
                    pos, cost, keys_collected, keys_required = frontier.pop()
                    visited.add(pos)
                    for direction in self.moves:
                        next_pos = pos + direction.value
                        if next_pos in self.walls or next_pos in visited:
                            continue
                        new_cost = cost + 1

                        try:
                            keys_required = keys_required | {self.doors[next_pos].name}
                        except KeyError:
                            pass

                        try:
                            key = self.keys[next_pos]
                            keys_collected = keys_collected | {key.name}
                            map_to[key] = new_cost, keys_collected, keys_required
                        except KeyError:
                            pass

                        frontier.add((next_pos, new_cost, keys_collected, keys_required))

                self.compressed[start] = map_to

    def get_neighbours(self, positions, keys):

        for i in range(len(positions)):
            for target, (cost, collected, required) in self.compressed[positions[i]].items():
                if not required.issubset(keys):
                    continue

                yield (positions[:i] + (target.pos,) + positions[i + 1 :], keys | collected), cost


with open(sys.argv[1], "r") as file:
    grid = Grid([line.strip() for line in file])

frontier = []
start = (grid.pos, frozenset())
heapq.heappush(frontier, (0, start))
came_from = {}
cost_so_far = {}
# came_from[start] = None
cost_so_far[start] = 0

while frontier:
    s, (pos, keys) = heapq.heappop(frontier)

    if len(keys) == len(grid.keys):
        # Got it!
        break

    for next_state, cost in grid.get_neighbours(pos, keys):
        new_cost = cost_so_far[pos, keys] + cost

        if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
            cost_so_far[next_state] = new_cost
            priority = new_cost + grid.heuristic(*next_state)
            heapq.heappush(frontier, (priority, next_state))
            # came_from[next_state] = pos, keys


else:
    print("Failed to find the path")
    raise Bad()


print(cost_so_far[pos, keys])
