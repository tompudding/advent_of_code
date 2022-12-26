import sys
import math


class Facing:
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


# in_to_rotation = {


def get_num(path):
    pos = 0
    while pos < len(path) and path[pos] in "0123456789":
        pos += 1
    return path[pos:], int(path[:pos])


class Grid:
    def __init__(self, lines, wrap=True):
        self.height = len(lines)
        self.width = max((len(line) for line in lines))
        self.grid = {}
        self.neighbours = {}
        self.start = None

        for row, line in enumerate(lines):
            first_col = last_col = None
            for col, char in enumerate(line):
                if char == " ":
                    continue

                if self.start is None:
                    self.start = (col, row)

                self.grid[(col, row)] = char
                self.neighbours[col, row] = {}
                if first_col is None:
                    first_col = col
                else:
                    self.neighbours[(col, row)][Facing.LEFT] = ((col - 1, row), 0)
                last_col = col
                self.neighbours[(col, row)][Facing.RIGHT] = ((col + 1, row), 0)
            if wrap:
                self.neighbours[(last_col, row)][Facing.RIGHT] = ((first_col, row), 0)
                self.neighbours[(first_col, row)][Facing.LEFT] = ((last_col, row), 0)
            else:
                del self.neighbours[(last_col, row)][Facing.RIGHT]

        for col in range(self.width):
            first_row = last_row = None
            for row in range(self.height):
                if (col, row) not in self.grid:
                    continue
                if first_row is None:
                    first_row = row
                else:
                    self.neighbours[(col, row)][Facing.UP] = ((col, row - 1), 0)
                last_row = row

                self.neighbours[(col, row)][Facing.DOWN] = ((col, row + 1), 0)
            if wrap:
                self.neighbours[(col, last_row)][Facing.DOWN] = ((col, first_row), 0)
                self.neighbours[(col, first_row)][Facing.UP] = ((col, last_row), 0)
            else:
                del self.neighbours[(col, last_row)][Facing.DOWN]

    def move(self, num):
        for i in range(num):
            next, rot = self.neighbours[self.pos][self.facing]
            if self.grid[next] == "#":
                return
            self.pos = next
            self.facing = (self.facing - rot) % 4

    def follow(self, path):
        self.facing = 0
        self.pos = self.start
        while path:
            path, num = get_num(path)
            self.move(num)
            if not path:
                break

            dir = path[0]
            if dir == "L":
                self.facing = (self.facing + 3) % 4
            elif dir == "R":
                self.facing = (self.facing + 1) % 4

            path = path[1:]

    def answer(self):
        return 1000 * (self.pos[1] + 1) + 4 * (self.pos[0] + 1) + self.facing


class Face:
    face_map = {
        1: {
            Facing.RIGHT: (5, Facing.UP),
            Facing.DOWN: (3, Facing.UP),
            Facing.LEFT: (2, Facing.DOWN),
            Facing.UP: (4, Facing.DOWN),
        },
        2: {
            Facing.RIGHT: (4, Facing.LEFT),
            Facing.DOWN: (1, Facing.LEFT),
            Facing.LEFT: (3, Facing.LEFT),
            Facing.UP: (6, Facing.DOWN),
        },
        3: {
            Facing.RIGHT: (5, Facing.LEFT),
            Facing.DOWN: (6, Facing.LEFT),
            Facing.LEFT: (2, Facing.LEFT),
            Facing.UP: (1, Facing.DOWN),
        },
        4: {
            Facing.RIGHT: (5, Facing.RIGHT),
            Facing.DOWN: (1, Facing.UP),
            Facing.LEFT: (2, Facing.RIGHT),
            Facing.UP: (6, Facing.RIGHT),
        },
        5: {
            Facing.RIGHT: (4, Facing.RIGHT),
            Facing.DOWN: (6, Facing.UP),
            Facing.LEFT: (3, Facing.RIGHT),
            Facing.UP: (1, Facing.RIGHT),
        },
        6: {
            Facing.RIGHT: (4, Facing.UP),
            Facing.DOWN: (2, Facing.UP),
            Facing.LEFT: (3, Facing.DOWN),
            Facing.UP: (5, Facing.DOWN),
        },
    }
    edge_steps = {Facing.RIGHT: (0, 1), Facing.DOWN: (-1, 0), Facing.LEFT: (0, -1), Facing.UP: (1, 0)}

    def __init__(self, cube, size, top_left, grid):
        self.cube = cube
        self.size = size
        self.top_left = top_left
        self.grid = grid
        self.neighbours = {}
        self.rotation = 0
        self.face_num = None
        self.edge_starts = {
            Facing.RIGHT: (self.top_left[0] + self.size - 1, self.top_left[1]),
            Facing.DOWN: (self.top_left[0] + self.size - 1, self.top_left[1] + self.size - 1),
            Facing.LEFT: (self.top_left[0], self.top_left[1] + self.size - 1),
            Facing.UP: self.top_left,
        }

        # At least one of our faces will be connected on init
        for dir, vector in (
            (Facing.RIGHT, (self.size, 0)),
            (Facing.DOWN, (0, self.size)),
            (Facing.LEFT, (-self.size, 0)),
            (Facing.UP, (0, -self.size)),
        ):
            pos = (self.top_left[0] + vector[0], self.top_left[1] + vector[1])
            if pos not in self.grid:
                continue
            self.neighbours[dir] = pos

    def __repr__(self):
        return f"Face {self.face_num} with rotation {self.rotation}"

    def label(self, face_num, rotation):
        self.face_num = face_num
        self.rotation = rotation

        self.neighbours = {(dir - self.rotation) % 4: face for dir, face in self.neighbours.items()}

        for dir, face in self.neighbours.items():
            if face.face_num is not None:
                continue
            num, in_dir = self.face_map[self.face_num][dir]
            face.label(face_num=num, rotation=(2 + dir + self.rotation - in_dir) % 4)

    def fill_out(self):
        # Once we're labelled, we want to update the neighbours with all the edges rather than the one or two
        # that are connected in the original map
        for dir, (fn, in_dir) in self.face_map[self.face_num].items():
            rel_dir = dir
            if rel_dir in self.neighbours:
                assert fn == self.neighbours[rel_dir].face_num
                # raise Bobbins1
                continue
            self.neighbours[rel_dir] = self.cube.faces[fn]
            pass

    def edge(self, dir):
        # Yield all the points along our edge
        abs_dir = (self.rotation + dir) % 4

        start = self.edge_starts[abs_dir]
        step = self.edge_steps[abs_dir]

        for i in range(self.size):
            yield (start[0] + step[0] * i, start[1] + step[1] * i)

    def edge_dir(self, dir):
        # Which direction is out?
        abs_dir = (self.rotation + dir) % 4
        return abs_dir

    def connect(self):
        # For each of our edges, we want to set up the neighbours correctly
        for dir, face in self.neighbours.items():
            num, in_dir = self.face_map[self.face_num][dir]
            outer = self.edge_dir(dir)
            rot = (2 + self.rotation - face.rotation + dir - in_dir) % 4

            for edge_point, other_edge_point in zip(self.edge(dir), reversed(list(face.edge(in_dir)))):
                outer = self.edge_dir(dir)

                try:
                    if self.cube.neighbours[edge_point][outer][0] != other_edge_point:
                        print(
                            f"Neighbour of {edge_point} in the direction {outer} is currently {self.cube.neighbours[edge_point][outer]}, but we're trying to set it to {other_edge_point}"
                        )
                        raise Bobbins
                except KeyError:
                    pass
                self.cube.neighbours[edge_point][outer] = (other_edge_point, rot)


class CubeGrid(Grid):
    def __init__(self, lines):
        super().__init__(lines, wrap=False)

        # How big are the faces?
        face_size = int(math.sqrt(len(self.grid) // 6))

        assert 6 * (face_size ** 2) == len(self.grid)

        # which of our grid faces are set?
        faces = []
        for col in range(self.width // face_size):
            for row in range(self.height // face_size):
                top_left = col * face_size, row * face_size
                if top_left in self.grid:
                    faces.append(Face(self, face_size, top_left, self.grid))

        for face in faces:
            new_neighbours = {}
            for dir, point in face.neighbours.items():
                neigh_face = [face for face in faces if face.top_left == point]
                assert len(neigh_face) == 1
                new_neighbours[dir] = neigh_face[0]
            face.neighbours = new_neighbours

        face = faces[0].label(1, rotation=0)

        self.faces = {face.face_num: face for face in faces}

        for face in faces:
            face.fill_out()
        for face in faces:
            face.connect()


grid_lines = []
with open(sys.argv[1], "r") as file:
    for line in file:
        line = line.strip("\n")

        if not line:
            break
        grid_lines.append(line)

    for line in file:
        instructions = line.strip()

grid = Grid(grid_lines)

grid.follow(instructions)
print(grid.answer())

cube_grid = CubeGrid(grid_lines)
cube_grid.follow(instructions)
print(cube_grid.answer())
