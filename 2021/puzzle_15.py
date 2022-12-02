import sys
import heapq


def heuristic(a, b):
    # Manhattan distance on a square grid
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# A* implementation stolen from red blob games https://www.redblobgames.com/pathfinding/a-star/introduction.html
class Grid:
    def __init__(self, filename):
        self.grid = {}

        with open(sys.argv[1], "r") as file:
            for row, line in enumerate(file):
                for col, char in enumerate(line.strip()):
                    self.grid[(col, row)] = int(char)

        # This is definitely the most efficient way to calculate the dimensions
        self.width = max((row for row, col in self.grid.keys())) + 1
        self.height = max((col for row, col in self.grid.keys())) + 1

    def get_neighbours(self, pos):
        for diff in (-1, 0), (1, 0), (0, 1), (0, -1):
            target = (pos[0] + diff[0], pos[1] + diff[1])

            if target[0] < 0 or target[0] >= self.width:
                continue

            if target[1] < 0 or target[1] >= self.height:
                continue

            yield target

    def get_path(self, start, end):
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while frontier:
            s, current = heapq.heappop(frontier)

            if current == end:
                break

            for next in self.get_neighbours(current):
                new_cost = cost_so_far[current] + self.grid[next]
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(end, next)
                    heapq.heappush(frontier, (priority, next))
                    came_from[next] = current

        # reconstruct the path
        current = end

        path = []
        cost = 0
        while current != start:
            cost += self.grid[current]
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path, cost

    def expand(self, scale):
        new_grid = {}
        for x in range(scale[0]):
            for y in range(scale[1]):
                for pos, cost in self.grid.items():
                    new_grid[pos[0] + self.width * x, pos[1] + self.height * y] = 1 + (cost + x + y - 1) % 9

        self.grid = new_grid
        self.width *= scale[0]
        self.height *= scale[1]

    def __repr__(self):
        out = []

        for y in range(self.height):
            out.append("".join((str(self.grid[x, y]) for x in range(self.width))))

        return "\n".join(out)


grid = Grid(sys.argv[1])

path, cost = grid.get_path((0, 0), (grid.width - 1, grid.height - 1))
print(cost)

grid.expand((5, 5))

path, cost = grid.get_path((0, 0), (grid.width - 1, grid.height - 1))
print(cost)
