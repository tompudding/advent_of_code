import sys
from dataclasses import dataclass
import collections
from utils import Point2D as Point
import heapq
import enum


class Directions:
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    ALL = [UP, RIGHT, DOWN, LEFT]


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


class Grid:
    moves = (Directions.UP, Directions.LEFT, Directions.RIGHT, Directions.DOWN)
    turns = {
        Directions.UP: (Directions.LEFT, Directions.RIGHT),
        Directions.RIGHT: (Directions.UP, Directions.DOWN),
        Directions.DOWN: (Directions.RIGHT, Directions.LEFT),
        Directions.LEFT: (Directions.DOWN, Directions.UP),
    }

    def __init__(self, lines):
        self.grid = {}
        self.walls = set()

        self.height = len(lines)
        self.width = len(lines[0])
        self.start = None

        for y, row in enumerate(lines):
            for x, char in enumerate(row):
                p = (x, y)
                self.grid[p] = char
                if char == ".":
                    continue
                if char == "#":
                    self.walls.add(p)
                elif char == "S":
                    self.start = p
                elif char == "E":
                    self.end = p
        self.spaces = self.grid.keys() - self.walls
        self.compress()

    def compress(self):
        # first get all the points with 3 paths
        nodes = {self.start, self.end}
        for p in self.spaces:
            neighbours = [add(p, direction) for direction in Directions.ALL]
            neighbours = [n for n in neighbours if n in self.spaces]
            if len(neighbours) >= 3:
                nodes.add(p)

        # Now we add the directions for each of those nodes.
        paths = collections.defaultdict(list)
        for node in nodes:
            for direction in Directions.ALL:

                start = (node, direction)
                pos = node
                cost = 0
                walked_nodes = set()
                while True:
                    walked_nodes.add(pos)
                    next_pos = add(pos, direction)

                    if next_pos in nodes:
                        # We're done
                        walked_nodes.add(next_pos)
                        paths[start].append(((next_pos, direction), cost + 1, walked_nodes))
                        break
                    elif next_pos in self.spaces:
                        cost += 1
                        pos = next_pos
                        continue
                    else:
                        # We need to turn
                        for turn in self.turns[direction]:
                            next_pos = add(pos, turn)
                            if next_pos in self.spaces:
                                direction = turn
                                cost += 1000
                                break
                        else:
                            # No turns allowed us to continue, there's no path here
                            break

                        continue

        # We also need the turn paths:
        for node in nodes:
            for direction in Directions.ALL:
                for turn in self.turns[direction]:
                    paths[node, direction].append(((node, turn), 1000, {node}))
        self.paths = paths

    def get_neighbours_old(self, pos, direction):
        # Try moving forward and backwards
        move_to = add(pos, direction)
        if move_to not in self.walls:
            yield ((move_to, direction), 1)

        # Then try turning
        for turn in self.turns[direction]:
            yield ((pos, turn), 1000)

    def get_neighbours(self, pos, direction):
        for next_state in self.paths[pos, direction]:
            yield next_state

    def heuristic(self, pos, direction):
        # This is not yet clear
        return 0

    def __repr__(self):
        out = []

        for y in range(self.height):
            line = []
            for x in range(self.width):
                p = (x, y)
                if p in self.walls:
                    char = "#"
                elif p in self.walked:
                    char = "O"
                elif p == self.start:
                    char = "S"
                elif p == self.end:
                    char = "E"
                else:
                    char = "."
                line.append(char)
            out.append("".join(line))
        return "\n".join(out)


with open(sys.argv[1], "r") as file:
    grid = Grid([line.strip() for line in file])


frontier = []
start = (grid.start, Directions.RIGHT)
heapq.heappush(frontier, (0, start))
came_from = collections.defaultdict(set)
cost_so_far = {}
came_from[start] = None
cost_so_far[start] = 0

while frontier:
    s, (pos, direction) = heapq.heappop(frontier)

    if pos == grid.end:
        # Got it!
        break

    for next_state, cost, walked_nodes in grid.get_neighbours(pos, direction):
        # print(pos, direction, "going to", next_state, cost)
        new_cost = cost_so_far[pos, direction] + cost

        if next_state not in cost_so_far or new_cost <= cost_so_far[next_state]:

            if next_state not in cost_so_far or new_cost == cost_so_far[next_state]:
                came_from[next_state].add((pos, direction, frozenset(walked_nodes)))
            else:
                came_from[next_state] = {(pos, direction, frozenset(walked_nodes))}
            cost_so_far[next_state] = new_cost
            priority = new_cost + grid.heuristic(*next_state)
            heapq.heappush(frontier, (priority, next_state))
else:
    print("Failed to find the path")
    raise Bad()

final = (pos, direction)
min_path_cost = cost_so_far[final]

print(min_path_cost)


def find_paths(pos, direction):
    out = set()

    if pos == grid.start:
        return out

    for parent_pos, parent_direction, walked_nodes in came_from[pos, direction]:
        a = find_paths(parent_pos, parent_direction)
        out |= a
        out |= walked_nodes

    return out


all_jawns = set()
for prev_pos, prev_direction, walked_nodes in came_from[final]:
    all_jawns |= walked_nodes | find_paths(prev_pos, prev_direction)
print(len(all_jawns))

# grid.walked = all_jawns
# print(grid)
