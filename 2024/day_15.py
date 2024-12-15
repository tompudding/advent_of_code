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


class Grid:
    def __init__(self, lines):
        self.grid = {}
        self.height = len(lines)
        self.width = len(lines[0])

        self.boxes = set()
        self.walls = set()
        self.robot = None

        for y, row in enumerate(lines):
            for x, char in enumerate(row):
                p = (x, y)
                if char == "#":
                    self.walls.add(p)
                elif char == "O":
                    self.boxes.add(p)
                elif char == "@":
                    self.robot = p

    def move_robot(self, direction):
        robot_pos = add(self.robot, direction.value)
        next_pos = robot_pos
        to_move = []

        while True:
            if next_pos in self.boxes:
                current_pos = next_pos
                next_pos = add(current_pos, direction.value)
                to_move.append((current_pos, next_pos))

            elif next_pos in self.walls:
                return
            else:
                # This is the free space
                break

        # Now everyone in robot and the to_move list move in direction
        for from_pos, to_pos in to_move:
            self.boxes.remove(from_pos)

        for from_pos, to_pos in to_move:
            self.boxes.add(to_pos)

        self.robot = robot_pos

    def get_gps(self):
        return sum((100 * y + x for (x, y) in self.boxes))

    def __repr__(self):
        out = []

        for y in range(self.height):
            line = []
            for x in range(self.width):
                p = (x, y)
                if p in self.walls:
                    char = "#"
                elif p in self.boxes:
                    char = "O"
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

for instruction in instructions:
    grid.move_robot(instruction)


print(grid.get_gps())
