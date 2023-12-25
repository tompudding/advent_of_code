import heapq
import sys


class Directions:
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

    adjacent = {UP, RIGHT, DOWN, LEFT}
    horizontal = {LEFT, RIGHT}
    vertical = {UP, DOWN}

    char = {UP: "^", RIGHT: ">", LEFT: "<", DOWN: "v"}
    slopes = {tile: direction for direction, tile in char.items()}


class PathPos:
    def __init__(self, pos):
        self.pos = pos
        self.data = pos

    def __add__(self, other):
        return self.__class__((self.pos[0] + other[0], self.pos[1] + other[1]))

    def __lt__(self, other):
        return self.data < other.data

    def __eq__(self, other):
        return self.data == other.data

    def __hash__(self):
        return hash(self.data)

    def __repr__(self):
        return f"pos={self.pos}"


class Node:
    def __init__(self, pos):
        self.edges = []
        self.pos = pos

    def add_edge(self, other, length):
        self.edges.append((other, length))

    def __repr__(self):
        out = [f"Node of {len(self.edges)} edges:"]

        for other, length in self.edges:
            out.append(f" {other.pos} {length=}")
        out.append("\n")

        return "\n".join(out)


class Grid:
    def __init__(self, lines):
        self.costs = {}

        self.height = len(lines)
        self.width = len(lines[0])

        self.rows = [list(line) for line in lines]
        self.tiles = {}
        self.start = self.end = None
        self.part_one = True

        for y, row in enumerate(lines):
            for x, char in enumerate(row):
                if y == 0 and char == ".":
                    self.start = PathPos((x, y))
                elif y == self.height - 1 and char == ".":
                    self.end = PathPos((x, y))
                self.tiles[PathPos((x, y))] = char

    def neighbours(self, pos, visited=None):
        options = Directions.adjacent
        tile = self.tiles[pos]

        if self.part_one:
            try:
                options = [Directions.slopes[tile]]
            except KeyError:
                pass

        for option in options:
            new_pos = pos + option

            if new_pos.pos[1] < 0 or new_pos.pos[1] >= self.height:
                continue

            if self.tiles[new_pos] == "#":
                continue

            if visited and new_pos in visited:
                continue

            yield new_pos

    def follow_grid(self, visited, node, so_far):

        best = 0

        for option, length in node.edges:

            if option.pos in visited:
                continue

            if option.pos == self.end:
                return so_far + length

            total = self.follow_grid(visited | {option.pos}, option, so_far + length)
            if total > best:
                best = total

        return best

    def walk_to_node(self, pos, start):
        length = 1
        for option in self.neighbours(pos):
            if option == start:
                # This is totally the wrong way
                continue

            last = pos
            while option not in self.nodes:
                try:
                    next = [new for new in self.neighbours(option) if new != last][0]
                except IndexError:
                    return None
                last = option
                option = next

                length += 1
            return self.nodes[option], length + 1

    def parse_grid(self):
        pos = self.start

        self.nodes = {}

        for pos, char in self.tiles.items():
            if char == "#":
                continue
            options = list(self.neighbours(pos))

            if len(options) > 2 or pos == self.start:
                self.nodes[pos] = Node(pos)

            if pos == self.end:
                self.nodes[pos] = Node(pos)
                self.end_node = self.nodes[pos]

        for node_pos, node in self.nodes.items():
            for option in self.neighbours(node.pos):
                result = self.walk_to_node(option, start=node.pos)
                if result is not None:
                    other_node, length = result
                    node.add_edge(other_node, length)

        print(self.follow_grid(set(), self.nodes[self.start], 0))


with open(sys.argv[1], "r") as file:
    grid = Grid([line.strip() for line in file])


grid.parse_grid()

grid.part_one = False

grid.parse_grid()
