import sys


class Directions:
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

    adjacent = {UP, RIGHT, DOWN, LEFT}
    horizontal = {LEFT, RIGHT}
    vertical = {UP, DOWN}


def add(pos, other):
    return (pos[0] + other[0], pos[1] + other[1])


def mirror_right(pos, direction):
    new_direction = {
        Directions.RIGHT: Directions.UP,
        Directions.UP: Directions.RIGHT,
        Directions.LEFT: Directions.DOWN,
        Directions.DOWN: Directions.LEFT,
    }[direction]
    return [(add(pos, new_direction), new_direction)]


def mirror_left(pos, direction):
    new_direction = {
        Directions.RIGHT: Directions.DOWN,
        Directions.DOWN: Directions.RIGHT,
        Directions.LEFT: Directions.UP,
        Directions.UP: Directions.LEFT,
    }[direction]
    return [(add(pos, new_direction), new_direction)]


def splitter_horiz(pos, direction):
    if direction in Directions.vertical:
        return [(add(pos, new_direction), new_direction) for new_direction in Directions.horizontal]
    return [(add(pos, direction), direction)]


def splitter_vert(pos, direction):
    if direction in Directions.horizontal:
        return [(add(pos, new_direction), new_direction) for new_direction in Directions.vertical]
    return [(add(pos, direction), direction)]


class Grid:
    obstacles = {"/": mirror_right, "\\": mirror_left, "-": splitter_horiz, "|": splitter_vert}

    def __init__(self, lines):
        self.rows = [list(line) for line in lines]
        self.height = len(self.rows)
        self.width = len(self.rows[0])
        self.grid = {
            (x, y): self.obstacles[self.rows[y][x]]
            for x in range(self.width)
            for y in range(self.height)
            if self.rows[y][x] != "."
        }

        self.visited = set()

    def follow_path(self, pos, direction):
        while (
            (pos, direction) not in self.visited
            and pos[0] >= 0
            and pos[0] < self.width
            and pos[1] >= 0
            and pos[1] < self.height
        ):
            self.visited.add((pos, direction))
            # print("P", pos, direction)

            try:
                obstacle = self.grid[pos]
                next_positions = obstacle(pos, direction)
            except KeyError:
                next_positions = (
                    (
                        add(pos, direction),
                        direction,
                    ),
                )

            pos, direction = next_positions[0]

            if len(next_positions) > 1:
                # print("***")
                self.follow_path(*next_positions[1])

    def energised_from_pos(self, pos, direction):
        self.visited = set()
        self.follow_path(pos, direction)
        return len({pos for pos, direction in grid.visited})

    def __repr__(self):
        out = []
        for y, row in enumerate(self.rows):
            out_row = []
            for x, char in enumerate(row):
                if any(((x, y), direction) in self.visited for direction in Directions.adjacent):
                    out_row.append("#")
                else:
                    out_row.append(char)
            out.append("".join(out_row))
        return "\n".join(out)


with open(sys.argv[1], "r") as file:
    lines = [line.strip() for line in file if line]

grid = Grid(lines)
print(grid.energised_from_pos((0, 0), Directions.RIGHT))

exterior = (
    # LEFT
    [((0, row), Directions.RIGHT) for row in range(grid.height)]
    # TOP
    + [((col, 0), Directions.DOWN) for col in range(grid.width)]
    # RIGHT
    + [((grid.width - 1, row), Directions.LEFT) for row in range(grid.height)]
    # BOTTOM
    + [((col, grid.height - 1), Directions.UP) for col in range(grid.width)]
)

best = max((grid.energised_from_pos(p, d) for (p, d) in exterior))
print(best)
