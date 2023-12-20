import sys


class OctoGrid:
    width = 10
    height = 10
    neighbours_diff = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue
            neighbours_diff.append((x, y))

    def __init__(self, lines):
        self.grid = {}

        for row, line in enumerate(lines):
            for col, char in enumerate(line.strip()):
                self.grid[col, row] = int(char)

            if row >= self.height:
                break

        self.flashed = set()
        self.num_flashed = 0

    def step(self):
        self.flashed = set()

        for (x, y) in self.grid:
            self.increment(x, y)

    def increment(self, x, y):
        if self.grid[x, y] == 9:
            self.flash(x, y)
        elif (x, y) not in self.flashed:
            self.grid[(x, y)] += 1

    def get_neighbours(self, x, y):
        for diff in self.neighbours_diff:
            pos = (x + diff[0], y + diff[1])
            if 0 <= pos[0] < self.width and 0 <= pos[1] < self.height:
                yield pos

    def flash(self, x, y):
        if (x, y) in self.flashed:
            return
        self.num_flashed += 1
        self.flashed.add((x, y))
        self.grid[x, y] = 0

        for neighbour in self.get_neighbours(x, y):
            self.increment(neighbour[0], neighbour[1])

    def __repr__(self):
        out = ["+" + ("-" * 10) + "+"]

        for y in range(self.height):
            out.append("|" + ("".join((f"{self.grid[x,y]}" for x in range(self.width)))) + "|")

        out.append("+" + ("-" * 10) + "+")
        return "\n".join(out)


with open(sys.argv[1], "r") as file:
    data = file.readlines()

grid = OctoGrid(data)
print(grid)

for i in range(100):
    grid.step()

print(f"{grid.num_flashed=}")

grid = OctoGrid(data)

count = 0
while len(grid.flashed) != 100:
    grid.step()
    count += 1

print(count)
