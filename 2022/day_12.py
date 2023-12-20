import sys

class Grid:
    def __init__(self, filename):
        self.grid = {}
        self.a_starts = []

        with open(sys.argv[1], "r") as file:
            for row, line in enumerate(file):
                for col, char in enumerate(line.strip()):
                    if char == 'S':
                        height = 1
                        self.start = (col, row)
                    elif char == 'E':
                        height = 26
                        self.end = (col, row)
                    else:
                        height = ord(char)-ord('a')+1

                    if height == 1:
                        self.a_starts.append((col, row))
                    self.grid[(col, row)] = height

        self.path_cache = {}

        self.height = row + 1
        self.width = col + 1

    def get_neighbours(self, pos):
        our_height = self.grid[pos]
        for diff in (-1, 0), (1, 0), (0, 1), (0, -1):
            target = (pos[0] + diff[0], pos[1] + diff[1])

            if target[0] < 0 or target[0] >= self.width:
                continue

            if target[1] < 0 or target[1] >= self.height:
                continue

            new_height = self.grid[target]

            # We make this path backwards so this is the condition for arriving at a square
            if new_height >= our_height - 1:
                yield target

    def paths(self, end, starts):
        frontier = [end]
        came_from = {end : None}

        while frontier:
           current = frontier.pop(0)
           for next in self.get_neighbours(current):
              if next not in came_from:
                 frontier.append(next)
                 came_from[next] = current

        best = None
        for start in starts:
            current = start
            cost = 0
            while current != end:
                cost += 1
                try:
                    current = came_from[current]
                except KeyError:
                    # No path reaches this one
                    cost = None
                    break
            if cost is None:
                continue
            if best is None or cost < best:
                best = cost

        return best


grid = Grid(sys.argv[1])

# Part 1
print(grid.paths(grid.end, (grid.start,)))

# Part 2
print(grid.paths(grid.end, grid.a_starts))
