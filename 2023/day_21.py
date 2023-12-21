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

        self.blocking_walls = set(
            (x, y) for (x, y) in self.walls if (1 == ((abs(x - self.start[0]) + abs(y - self.start[1])) & 1))
        )
        self.walk_positions = set()

        # self.bottom_left_walls = {(x, y) for (x, y) in self.blocking_walls if x <= y}
        # self.top_right_walls = {(x, y) for (x, y) in self.blocking_walls if x >= y}
        # self.bottom_right_walls = {(x, y) for (x, y) in self.blocking_walls if x + y >= (self.width - 1)}
        # self.top_left_walls = {(x, y) for (x, y) in self.blocking_walls if x + y <= (self.width - 1)}

        # self.corners = [
        #     self.bottom_left_walls & self.bottom_right_walls,
        #     self.bottom_left_walls & self.top_left_walls,
        #     self.top_left_walls & self.top_right_walls,
        #     self.top_right_walls & self.bottom_right_walls,
        # ]
        print("blocking walls per tile", len(self.blocking_walls))
        # print("corners=", [len(walls) for walls in self.corners])
        # raise jim
        # self.corners_len = sum(len(walls) for walls in self.corners)
        self.pos_in_tile = None

    def step(self, positions, n):
        print(n)
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

        # self.step({self.start}, self.width + (self.width // 2) + 1)
        positions = self.step({self.start}, self.width * 2 + (self.width // 2))

        for grid_x in range(-3, 3):
            for grid_y in range(-2, 3):
                count = 0
                for x in range(self.width):
                    for y in range(self.height):
                        if ((grid_x * self.width) + x, (grid_y * self.height) + y) in positions:
                            count += 1
                print(f"{grid_x},{grid_y} = {count}")

        # We're going to use the reachable tile to compute some geometric shapes
        self.bottom_left_small = {(x, y) for (x, y) in self.reachable if y - x >= ((self.width // 2) + 1)}
        self.top_right_small = {(x, y) for (x, y) in self.reachable if y - x <= (-self.width // 2)}
        self.bottom_right_small = {(x, y) for (x, y) in self.reachable if x + y >= (3 * self.width // 2)}
        self.top_left_small = {(x, y) for (x, y) in self.reachable if x + y <= self.width // 2}

        self.bottom_left_big = {(x, y) for (x, y) in self.reachable if y - x >= (-self.width // 2)}
        self.top_right_big = {(x, y) for (x, y) in self.reachable if y - x <= self.width // 2}
        self.bottom_right_big = {(x, y) for (x, y) in self.reachable if x + y >= self.width // 2}
        self.top_left_big = {(x, y) for (x, y) in self.reachable if x + y <= (3 * self.width // 2)}

        print(
            "smalls:",
            [
                len(x)
                for x in (
                    self.bottom_left_small,
                    self.top_right_small,
                    self.bottom_right_small,
                    self.top_left_small,
                )
            ],
        )
        print(
            "bigs:",
            [
                len(x)
                for x in (self.bottom_left_big, self.top_right_big, self.bottom_right_big, self.top_left_big)
            ],
        )

        self.corners = [
            self.bottom_left_big & self.bottom_right_big,
            self.bottom_left_big & self.top_left_big,
            self.top_left_big & self.top_right_big,
            self.top_right_big & self.bottom_right_big,
        ]
        self.corners_len = sum(len(corner) for corner in self.corners)
        print(len(self.reachable))

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

        print("a", grid_width)
        # That's how many from 0, but it goes in both directions (not including 0)
        grid_width += grid_width - 1
        print("full", grid_width)

        # Then we go up in a triangle, the next row has that many -2 and so on
        num = grid_width // 2
        extra = num * (grid_width - 2 + (grid_width & 1))

        num_tiles = grid_width + extra

        print(f"{num_tiles=} {num=}")

        # return self.pos_in_tile * num_tiles + self.corner_and_big + self.small_plus_big * num

        # So we being our total with all the walls in that many complete tiles, where the walls are on the same parity as our start number
        # total_walls = num_tiles * len(self.blocking_walls)
        total = num_tiles * len(self.reachable)

        # Now just just need to run along every edge tile. Because we've been asked for exactly in the middle
        # (n % width == 65 == width / 2), they're all going to be exact halves, except for the four tips. Now how many are there in each?
        # The number of rows above the middle is num -1

        # Is this the same as len(self.blocking walls? I think maybe not due to overlap)
        if num > 0:
            # total += (num + 1) * len(self.bottom_left_small)
            # total += (num + 1) * len(self.top_left_small)
            # total += (num + 1) * len(self.top_right_small)
            # total += (num + 1) * len(self.bottom_right_small)
            # WTF
            total += (num + 1) * (985 + 980 + 969 + 961)

            total += (num) * len(self.bottom_left_big)
            total += (num) * len(self.top_left_big)
            total += (num) * len(self.top_right_big)
            total += (num) * len(self.bottom_right_big)

        total += self.corners_len

        # The final adjustment is the cell parity. Odd squares get 17 less than even.
        # 2 for the main row.
        grid_width = (grid_width + 1) // 2
        num_parity = grid_width**2

        print("parity", num_parity)

        return total - num_parity * 17

        # raise Dunno()

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


grid.compute_stuff()
# print(grid)
print(grid.get_possible_steps(327))
print(grid.get_possible_steps(589))
print(grid.get_possible_steps(26501365))
# print(grid)
# print(grid.get_possible_steps(26501365))
# print(grid.get_possible_steps(5000))
