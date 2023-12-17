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


def heuristic(a, b):
    # Manhattan distance on a square grid
    return abs(a.pos[0] - b.pos[0]) + abs(a.pos[1] - b.pos[1])


class PathPosPart1:
    def __init__(self, pos, dir, num):
        self.pos = pos
        self.dir = dir
        self.data = (pos, dir, num)
        self.num_in_dir = num
        if dir is None:
            self.prohibited = set()
        else:
            self.prohibited = {(-dir[0], -dir[1])}

        if pos[0] == 0:
            self.prohibited.add(Directions.LEFT)
        elif pos[0] == grid.width - 1:
            self.prohibited.add(Directions.RIGHT)

        if pos[1] == 0:
            self.prohibited.add(Directions.UP)
        elif pos[1] == grid.height - 1:
            self.prohibited.add(Directions.DOWN)

        # If we've done 3 in a row we cannot go in that direction any more

        if self.num_in_dir >= 3:
            self.prohibited.add(self.dir)

    def can_stop(self):
        return True

    def __add__(self, other):
        return self.__class__(
            (self.pos[0] + other[0], self.pos[1] + other[1]),
            other,
            (self.num_in_dir + 1) if other == self.dir else 1,
        )

    def __lt__(self, other):
        return self.pos < other.pos

    def __repr__(self):
        return f"pos={self.pos} dir={self.dir} num_in_dir={self.num_in_dir}"


class PathPosPart2(PathPosPart1):
    def __init__(self, pos, dir, num):
        self.pos = pos
        self.dir = dir
        self.data = (pos, dir, num)
        self.num_in_dir = num
        if dir is None:
            self.prohibited = set()
        else:
            self.prohibited = {(-dir[0], -dir[1])}

        if pos[0] == 0:
            self.prohibited.add(Directions.LEFT)
        elif pos[0] == grid.width - 1:
            self.prohibited.add(Directions.RIGHT)

        if pos[1] == 0:
            self.prohibited.add(Directions.UP)
        elif pos[1] == grid.height - 1:
            self.prohibited.add(Directions.DOWN)

        if dir is not None and self.num_in_dir < 4:
            self.prohibited |= Directions.adjacent - {self.dir}
        elif self.num_in_dir >= 10:
            self.prohibited.add(self.dir)

    def can_stop(self):
        return self.num_in_dir >= 4


class Grid:
    def __init__(self, lines):
        self.costs = {}

        self.height = len(lines)
        self.width = len(lines[0])

        for y, row in enumerate(lines):
            for x, num in enumerate(row):
                self.costs[x, y] = int(num)

        self.last_path = {}

    def __repr__(self):
        out = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                try:
                    path_pos = self.last_path[x, y]
                    char = Directions.char[path_pos.dir]
                except KeyError:
                    char = f"{self.costs[x, y]}"
                row.append(char)

            out.append("".join(row))

        return "\n".join(out)

    def neighbours(self, pos):
        for adjust in Directions.adjacent - pos.prohibited:
            yield pos + adjust

    def get_path(self, start, end, cls):
        frontier = []
        # The dir is arbitrary here since the num is 0
        start = cls(start, None, 0)
        end = cls(end, Directions.DOWN, 0)
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start.data] = None
        cost_so_far[start.data] = 0

        while frontier:
            s, current = heapq.heappop(frontier)

            if current.pos == end.pos and current.can_stop():
                end = current
                break

            for next in self.neighbours(current):
                new_cost = cost_so_far[current.data] + self.costs[next.pos]
                # print(current, next, new_cost)
                if next.data not in cost_so_far or new_cost < cost_so_far[next.data]:
                    cost_so_far[next.data] = new_cost
                    priority = new_cost + heuristic(end, next)
                    heapq.heappush(frontier, (priority, next))
                    came_from[next.data] = current

        current = end
        path = [current]

        while next := came_from[current.data]:
            path.append(next)
            current = next

        self.last_path = {pos.pos: pos for pos in path}
        return list(reversed(path)), cost_so_far[end.data]


with open(sys.argv[1], "r") as file:
    grid = Grid([line.strip() for line in file])

print(grid)

path, cost = grid.get_path((0, 0), (grid.width - 1, grid.height - 1), PathPosPart1)
# path = grid.get_path((0, 0), (6, 6))
print()

print(grid)

print(cost)


path, cost = grid.get_path((0, 0), (grid.width - 1, grid.height - 1), PathPosPart2)
# path = grid.get_path((0, 0), (6, 6))

print(grid)

print(len(path), cost)
