import sys


class RightWall:
    char = "R"
    is_horizontal = True

    def __init__(self, length, colour):
        self.length = length
        self.colour = colour

        data = int(colour.strip("()#"), 16)
        self.real_length = data >> 4
        print(self.real_length)

    def generate(self, x, y):
        self.end_pos = (x + self.length, y)
        return {(x + i, y) for i in range(0, self.length)}


class LeftWall(RightWall):
    char = "L"
    is_horizontal = True

    def generate(self, x, y):
        self.end_pos = (x - self.length, y)
        return {(x - i, y) for i in range(1, self.length + 1)}


class UpWall(RightWall):
    char = "U"
    is_horizontal = False

    def generate(self, x, y):
        self.end_pos = (x, y - self.length)
        return {(x, y - i) for i in range(0, self.length)}


class DownWall(UpWall):
    char = "D"
    is_horizontal = False

    def generate(self, x, y):
        self.end_pos = (x, y + self.length)
        return {(x, y + i) for i in range(1, self.length + 1)}


class Quarry:
    def __init__(self, walls):
        pos = (0, 0)

        self.walls = walls
        self.horizontal_walls = set()
        self.vertical_walls = set()
        caps = set()

        for wall in walls:
            target = self.horizontal_walls if wall.is_horizontal else self.vertical_walls
            target |= wall.generate(*pos)
            pos = wall.end_pos
            caps.add(pos)

        self.all_walls = self.horizontal_walls | self.vertical_walls | caps
        self.top_left = min(x for x, y in self.all_walls), min(y for x, y in self.all_walls)
        self.bottom_right = max(x for x, y in self.all_walls), max(y for x, y in self.all_walls)
        print(f"{self.top_left=} {self.bottom_right=}")

        x_odd = set()
        y_odd = set()
        # Fill in the interior

        for y in range(self.top_left[1], self.bottom_right[1] + 1):
            parity = 0
            for x in range(self.top_left[0], self.bottom_right[0] + 1):
                if (x, y) in self.vertical_walls:
                    parity += 1
                    continue
                if parity & 1:
                    x_odd.add((x, y))

        for x in range(self.top_left[0], self.bottom_right[0] + 1):
            parity = 0
            for y in range(self.top_left[1], self.bottom_right[1] + 1):
                if (x, y) in self.horizontal_walls:
                    parity += 1
                    continue
                if parity & 1:
                    y_odd.add((x, y))

        print((3, 2) in x_odd, (3, 2) in y_odd)
        self.interior = x_odd & y_odd

    def get_capacity(self):
        return len(self.interior | self.all_walls)

    def __repr__(self):
        out = []

        for y in range(self.top_left[1], self.bottom_right[1] + 1):
            row = []
            for x in range(self.top_left[0], self.bottom_right[0] + 1):
                char = "."

                if (x, y) in self.all_walls:
                    char = "#"
                elif (x, y) in self.interior:
                    char = "x"
                row.append(char)
            out.append("".join(row))
        return "\n".join(out)


wall_lookup = {wall.char: wall for wall in (RightWall, UpWall, DownWall, LeftWall)}

with open(sys.argv[1], "r") as file:
    walls = []
    for line in file:
        wall_type, length, colour = line.strip().split()
        walls.append(wall_lookup[wall_type](int(length), colour))

quarry = Quarry(walls)
print(quarry)
print(quarry.get_capacity())

for wall in walls:
    print(wall.real_length)
