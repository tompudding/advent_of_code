import sys


class Directions:
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

    adjacent = {UP, RIGHT, DOWN, LEFT}


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


class Grid:
    def __init__(self, lines):
        self.height = len(lines)
        self.width = len(lines[0])
        self.walls = set()

        for y, row in enumerate(lines):
            for x, char in enumerate(row):
                if char == "S":
                    self.start = (x, y)
                elif char == "#":
                    self.walls.add((x, y))

    def step(self, positions, n):
        for i in range(n):
            new_positions = set()

            for pos in positions:
                for off in Directions.adjacent:
                    new_pos = add(pos, off)

                    if (new_pos[0] % self.width, new_pos[1] % self.height) in self.walls:
                        continue

                    new_positions.add(new_pos)

            positions = new_positions

        self.reachable = {
            (x, y) for (x, y) in positions if x >= 0 and x < self.width and y >= 0 and y < self.height
        }

        return positions

    def compute_stuff(self):
        # We know the number of blocking walls in each grid tile, but we want to know the number in each of
        # the four corner pieces, as well as each of the four types of small diagonals, and the four types of
        # big diagonals

        positions = self.step({self.start}, self.width * 2 + (self.width // 2))
        grid_counts = {}

        for grid_x in range(-3, 3):
            for grid_y in range(-2, 3):
                count = 0
                for x in range(self.width):
                    for y in range(self.height):
                        if ((grid_x * self.width) + x, (grid_y * self.height) + y) in positions:
                            count += 1
                grid_counts[grid_x, grid_y] = count

        self.smalls = sum(grid_counts[x, y] for (x, y) in ((-1, -2), (1, -2), (2, 1), (-2, 1)))
        self.bigs = sum(grid_counts[x, y] for (x, y) in ((-1, -1), (1, -1), (1, 1), (-1, 1)))
        self.corners = sum(grid_counts[x, y] for (x, y) in ((0, -2), (2, 0), (0, 2), (-2, 0)))
        self.num_even = grid_counts[0, 0]
        self.num_odd = grid_counts[0, 1]

    def get_possible_steps(self, n):
        if n < self.width:
            # We can just work them out
            self.walk_positions = grid.step({self.start}, n)
            return len(self.walk_positions)

        # For part 2 let's try working out the number of positions in the large walkable diamond, and then
        # subtracting the positions of the walls in that set. The number of walls is the hard part

        # diamond_size = (n + 1) ** 2

        # Firstly for the walls, let's consider how many complete copies are entirely within our diamond.

        # At its widest, the last whole grid we're going to get not the one that the tip appears in, but it might be the previous one,
        # provided that the tip appears at least width / 2 into it (we're assuming width and height are at least similar)
        #
        # -----|-----|-----o
        #      |     |     |o
        #      |     |     o o
        #      |     |     |o
        # -----|-----|-----o

        grid_width = (self.start[0] + n) // self.width

        # That's how many from 0, but it goes in both directions (not including 0)
        grid_width += grid_width - 1

        # Then we go up in a triangle, the next row has that many -2 and so on
        num = grid_width // 2

        total = (num + 1) * self.smalls
        total += num * self.bigs

        total += self.corners

        # The final adjustment is the cell parity. Half or so of the tiles are "odd", and half are "even"
        # 2 for the main row.
        total += self.num_odd * (((grid_width + 1) // 2) ** 2)
        total += self.num_even * ((grid_width // 2) ** 2)
        return total

    def __repr__(self):
        out = []
        for y in range(-self.height * 1, self.height * 2):
            row = []
            for x in range(-self.width * 1, self.width * 2):
                if x % self.width == 0:
                    char = "|"
                elif y % self.height == 0:
                    char = "-"

                elif (x % self.width, y % self.height) in self.walls:
                    char = "#"
                elif (x, y) in self.walk_positions:
                    char = "O"
                elif (x, y) == self.start:
                    char = "S"
                else:
                    if (x % self.width, y % self.height) in self.corners[3]:
                        char = "X"
                    else:
                        char = "."

                row.append(char)

            out.append("".join(row))

        return "\n".join(out)


with open(sys.argv[1], "r") as file:
    grid = Grid([line.strip() for line in file])


print(grid.get_possible_steps(64))

grid.compute_stuff()


print(grid.get_possible_steps(26501365))
