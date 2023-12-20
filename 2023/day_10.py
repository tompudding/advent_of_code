import sys
import enum


def add(pos, other):
    return (pos[0] + other[0], pos[1] + other[1])


def subtract(pos, other):
    return (pos[0] - other[0], pos[1] - other[1])


class Directions:
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

    adjacent = {UP, RIGHT, DOWN, LEFT}


class Segments:
    TOP_RIGHT = add(Directions.UP, Directions.RIGHT)
    TOP_LEFT = add(Directions.UP, Directions.LEFT)
    BOTTOM_RIGHT = add(Directions.DOWN, Directions.RIGHT)
    BOTTOM_LEFT = add(Directions.DOWN, Directions.LEFT)

    adjacent = {(0, -2), (2, 0), (0, 2), (-2, 0)}

    bitfield = {
        TOP_RIGHT: 1 << 0,
        TOP_LEFT: 1 << 1,
        BOTTOM_RIGHT: 1 << 2,
        BOTTOM_LEFT: 1 << 3,
    }

    ALL = 0xF


class Point:
    # A point is a grid coord, and a segment like:
    #
    # +-----+
    # |  |  |
    # | -+- |
    # |  |  |
    # +-----+
    #
    def __init__(self, pos, segment):
        self.pos = pos
        self.segment = segment

        self.fields = (pos, segment)

    def neighbours(self):
        for direction in Segments.adjacent:
            new_segment = add(self.segment, direction)
            pos_x = 0
            pos_y = 0
            seg_x = new_segment[0]
            seg_y = new_segment[1]

            if abs(seg_x) == 3:
                pos_x = seg_x // 3
                seg_x = -pos_x

            if abs(seg_y) == 3:
                pos_y = seg_y // 3
                seg_y = -pos_y

            yield (Point((self.pos[0] + pos_x, self.pos[1] + pos_y), (seg_x, seg_y)))

    def __hash__(self):
        return hash(self.fields)

    def __eq__(self, other):
        return self.fields == other.fields

    def __repr__(self):
        return f"Point(pos={self.pos=}, segment={self.segment}"


class Pipe:
    translate = {"L": "└", "F": "┌", "J": "┘", "7": "┐", "|": "│", "-": "─", ".": " "}

    connects = {
        "│": {Directions.UP, Directions.DOWN},
        "─": {Directions.LEFT, Directions.RIGHT},
        "└": {Directions.UP, Directions.RIGHT},
        "┌": {Directions.DOWN, Directions.RIGHT},
        "┘": {Directions.LEFT, Directions.UP},
        "┐": {Directions.LEFT, Directions.DOWN},
        " ": set(),
    }

    bolden = {
        "│": "┃",
        "─": "━",
        "└": "┗",
        "┌": "┏",
        "┘": "┛",
        "┐": "┓",
    }

    def __init__(self, pos, char):
        try:
            char = self.translate[char]
        except KeyError:
            pass

        self.char = char
        self.pos = pos
        self.is_loop = False
        self.is_exterior = False
        try:
            self.bold = self.bolden[char]
        except KeyError:
            self.bold = char

        if char != "S":
            self.connects_to = {add(self.pos, direction) for direction in self.connects[self.char]}
        else:
            # We have to work this out later
            self.connects_to = {}

    def __repr__(self):
        if self.is_loop:
            return self.bold

        if self.is_exterior:
            return "O"

        else:
            return "I"


class Grid:
    blocks = {
        "│": {Segments.TOP_LEFT: {Segments.TOP_RIGHT}, Segments.BOTTOM_LEFT: {Segments.BOTTOM_RIGHT}},
        "─": {Segments.TOP_LEFT: {Segments.BOTTOM_LEFT}, Segments.TOP_RIGHT: {Segments.BOTTOM_RIGHT}},
        "└": {Segments.TOP_RIGHT: {Segments.TOP_LEFT, Segments.BOTTOM_RIGHT}},
        "┌": {Segments.BOTTOM_RIGHT: {Segments.TOP_RIGHT, Segments.BOTTOM_LEFT}},
        "┘": {Segments.TOP_LEFT: {Segments.TOP_RIGHT, Segments.BOTTOM_LEFT}},
        "┐": {Segments.BOTTOM_LEFT: {Segments.TOP_LEFT, Segments.BOTTOM_RIGHT}},
        " ": {},
    }

    def __init__(self, lines):
        self.connects_to = {}
        self.connects_from = {}
        self.grid = {}
        self.start = None

        self.rows = []

        for block_list in self.blocks.values():
            new_blocks = {}
            for frm, to in block_list.items():
                for seg in to:
                    try:
                        new_blocks[seg].add(frm)
                    except KeyError:
                        new_blocks[seg] = {frm}

            block_list |= new_blocks

        for row, line in enumerate(lines):
            current_row = []
            for col, char in enumerate(line):
                pos = (col, row)
                pipe = Pipe(pos, char)
                current_row.append(pipe)
                if pipe.char == "S":
                    self.start = pos
                self.grid[col, row] = pipe

                try:
                    self.connects_from[col, row] |= pipe.connects_to
                except KeyError:
                    self.connects_from[col, row] = set(pipe.connects_to)

                for other in pipe.connects_to:
                    try:
                        self.connects_to[other].add(pos)
                    except KeyError:
                        self.connects_to[other] = {pos}
            self.rows.append(current_row)

        # Now we can find what the start is connected to and fill that in
        start_pipe = self.grid[self.start]
        start_pipe.connects_to = self.connects_to[self.start]
        start_pipe.is_loop = True

        start_shape = {subtract(other, start_pipe.pos) for other in start_pipe.connects_to}

        for char, connects_to in Pipe.connects.items():
            if start_shape == connects_to:
                start_pipe.char = char
                break
        else:
            raise Exception("Start pipe is weird")

        self.width = len(self.rows[0])
        self.height = len(self.rows)

        # Find the one loop
        self.loop = self.find_loop()
        self.loop_tiles = set(self.loop)

        self.exterior = self.find_exterior()

        for tile in self.exterior:
            self.grid[tile].is_exterior = True

        self.num_interior = (self.width * self.height) - len(self.exterior | self.loop_tiles)

    def get_neighbours(self, pos):
        final = set()

        for point in pos.neighbours():
            if point.pos == pos.pos:
                # This means going back into the current square other side
                # We can only do this if permitted by the loop_tile in this square
                if pos.pos in self.loop_tiles:
                    blockers = self.blocks[self.grid[pos.pos].char]

                    try:
                        if point.segment in blockers[pos.segment]:
                            continue
                    except KeyError:
                        pass

            else:
                # We're flipping segment but moving pos
                if (
                    point.pos[0] < 0
                    or point.pos[0] >= self.width
                    or point.pos[1] < 0
                    or point.pos[1] >= self.height
                ):
                    continue

            final.add(point)

        return final

    def find_exterior(self):
        # The frontier starts as all the edge tiles that aren't in the path

        frontier = (
            # Left
            {Point((0, row), Segments.TOP_LEFT) for row in range(self.height)}
            | {Point((0, row), Segments.BOTTOM_LEFT) for row in range(self.height)}
            # Top
            | {Point((col, 0), Segments.TOP_LEFT) for col in range(self.width)}
            | {Point((col, 0), Segments.TOP_RIGHT) for col in range(self.width)}
            # Right
            | {Point((self.width - 1, row), Segments.TOP_RIGHT) for row in range(self.height)}
            | {Point((self.width - 1, row), Segments.BOTTOM_RIGHT) for row in range(self.height)}
            # Bottom
            | {Point((col, self.height - 1), Segments.BOTTOM_LEFT) for col in range(self.width)}
            | {Point((col, self.height - 1), Segments.BOTTOM_RIGHT) for col in range(self.width)}
        )

        exterior = set(frontier)
        examined = set()

        while frontier:
            current = frontier.pop()
            examined.add(current)
            exterior.add(current)
            new = self.get_neighbours(current)
            exterior |= new

            frontier |= new - examined

        # The final step of this is to or together the segments and only take the ones that have all four segments represented
        segments_map = {}

        for point in exterior:
            try:
                segments_map[point.pos] |= Segments.bitfield[point.segment]
            except KeyError:
                segments_map[point.pos] = Segments.bitfield[point.segment]

        return {pos for pos, mask in segments_map.items() if mask == Segments.ALL}

    def find_loop(self):
        # We start at the start, pick one of the directions, and then follow the path until we're back at the start
        steps = self.grid[self.start].connects_to
        assert len(steps) == 2
        pos = next(iter(steps))

        path = [self.start, pos]
        self.grid[pos].is_loop = True

        while pos != self.start:
            steps = self.grid[pos].connects_to - {path[-2]}
            assert len(steps) == 1
            pos = steps.pop()
            self.grid[pos].is_loop = True
            if pos == self.start:
                break
            path.append(pos)

        return path

    def find_furthest_point(self):
        return len(self.loop) // 2

    def __repr__(self):
        out = []
        for row in self.rows:
            out.append("".join((str(char) for char in row)))
        return "\n".join(out)


with open(sys.argv[1], "r") as file:
    lines = [line.strip() for line in file]

grid = Grid(lines)

print(grid)

print(grid.find_furthest_point())
print(grid.num_interior)
