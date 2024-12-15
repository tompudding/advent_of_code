import sys
import collections
import enum


class Directions(enum.Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


to_dir = {"^": Directions.UP, "<": Directions.LEFT, ">": Directions.RIGHT, "v": Directions.DOWN}


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


class Box:
    def __init__(self, pos_a, pos_b):
        self.pos = pos_a
        self.rest = pos_b
        self.positions = {pos_a, pos_b}

    def move(self, direction):
        return Box(add(self.pos, direction), add(self.rest, direction))

    def __hash__(self):
        return hash((self.pos, self.rest))

    def __eq__(self, other):
        return (self.pos, self.rest) == (other.pos, other.rest)


class Grid:
    def __init__(self, lines):
        self.grid = {}
        self.height = len(lines)
        self.width = len(lines[0] * 2)

        self.boxes = {}
        self.walls = set()
        self.robot = None

        for y, row in enumerate(lines):
            for x_pos, char in enumerate(row):
                x = x_pos * 2
                p_a = (x, y)
                p_b = (x + 1, y)
                if char == "#":
                    self.walls |= {p_a, p_b}
                elif char == "O":
                    self.boxes[p_a] = self.boxes[p_b] = Box(p_a, p_b)
                elif char == "@":
                    self.robot = p_a

    def move_robot(self, direction):
        robot_pos = add(self.robot, direction.value)
        frontier = {robot_pos}
        moving = set()

        # The frontier is everything that will impact another box when moved

        while True:
            to_add = set()
            for pos in frontier:
                if pos in self.walls:
                    return
                try:
                    box = self.boxes[pos]
                    new_box = box.move(direction.value)
                    to_add |= new_box.positions
                    moving.add((box, new_box))
                except KeyError:
                    pass

            if to_add.issubset(frontier):
                break
            else:
                frontier |= to_add
                # print(frontier)

        # We didn't run into any obstacles, so we can move everything in the list
        for box, new_box in moving:
            del self.boxes[box.pos]
            del self.boxes[box.rest]

        for box, new_box in moving:
            self.boxes[new_box.pos] = new_box
            self.boxes[new_box.rest] = new_box

        self.robot = robot_pos

    def get_gps(self):
        boxes = set(self.boxes.values())
        return sum((100 * box.pos[1] + box.pos[0] for box in boxes))

    def __repr__(self):
        out = []

        for y in range(self.height):
            line = []
            for x in range(self.width):
                p = (x, y)
                if p in self.walls:
                    char = "#"
                elif p in self.boxes:
                    box = self.boxes[p]
                    char = "[" if p == box.pos else "]"
                elif p == self.robot:
                    char = "X"
                else:
                    char = "."
                line.append(char)
            out.append("".join(line))
        return "\n".join(out)


with open(sys.argv[1], "r") as file:
    grid_lines, instruction_lines = file.read().split("\n\n")

    grid = Grid(grid_lines.splitlines())
    instructions = [to_dir[c] for c in "".join(instruction_lines.splitlines())]

print(grid)

for instruction in instructions:
    # print(f"{instruction}:")
    grid.move_robot(instruction)
    # print(grid)
    # print("-" * 80)


print(grid.get_gps())
