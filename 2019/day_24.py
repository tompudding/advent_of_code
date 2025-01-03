import sys
import enum
from collections import defaultdict


class Directions(enum.Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def neighbours(pos):
    for direction in Directions:
        yield add(pos, direction.value)


class Eris:
    WIDTH = 5
    HEIGHT = 5
    CENTRE = (2, 2)

    def __init__(self, lines):
        self.bugs = set()
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == "#":
                    self.bugs.add((x, y))
        self.bugs = frozenset(self.bugs)

    def step(self):
        new_bugs = set()
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                current = (x, y)
                count = sum(pos in self.bugs for pos in self.neighbours(current))

                if current in self.bugs:
                    if count == 1:
                        new_bugs.add(current)

                else:
                    if count in (1, 2):
                        new_bugs.add(current)
        self.bugs = frozenset(new_bugs)

    def neighbours(self, pos):
        for neighbour in neighbours(pos):
            yield neighbour

    def biodiversity(self):
        return sum(1 << (y * 5 + x) for x, y in self.bugs)


class PlutonianEris(Eris):

    def __init__(self, lines):
        super().__init__(lines)

        assert self.CENTRE not in self.bugs

        self.layers = {0: self.bugs}

        self.top_layer = 0
        self.bottom_layer = 0

        self.TOP = {(i, 0) for i in range(self.WIDTH)}
        self.RIGHT = {(self.WIDTH - 1, i) for i in range(self.HEIGHT)}
        self.BOTTOM = {(i, self.HEIGHT - 1) for i in range(self.WIDTH)}
        self.LEFT = {(0, i) for i in range(self.HEIGHT)}
        self.OUTER_EDGE = self.TOP | self.RIGHT | self.BOTTOM | self.LEFT
        self.INNER_EDGE = set(neighbours(self.CENTRE))

        self.outer_transitions = (
            {x: self.LEFT for x in self.RIGHT}
            | {x: self.RIGHT for x in self.LEFT}
            | {x: self.TOP for x in self.BOTTOM}
            | {x: self.BOTTOM for x in self.TOP}
        )

        self.inner_transitions = {
            Directions.DOWN.value: self.TOP,
            Directions.RIGHT.value: self.LEFT,
            Directions.LEFT.value: self.RIGHT,
            Directions.UP.value: self.BOTTOM,
        }

    def step(self):

        # Firstly we may need new layers, let's examine that so that our logic will be simpler
        if any(pos in self.layers[self.top_layer] for pos in self.OUTER_EDGE):
            self.top_layer += 1
            self.layers[self.top_layer] = set()

        if any(pos in self.layers[self.bottom_layer] for pos in self.INNER_EDGE):
            self.bottom_layer -= 1
            self.layers[self.bottom_layer] = set()

        new_layers = {}
        for depth in self.layers:
            new_bugs = set()
            for y in range(self.HEIGHT):
                for x in range(self.WIDTH):
                    current = (x, y)
                    count = 0
                    for depth_change, (x, y) in self.neighbours(current):
                        if (
                            depth + depth_change in self.layers
                            and (x, y) in self.layers[depth + depth_change]
                        ):
                            count += 1
                    if current in self.bugs:
                        if count == 1:
                            new_bugs.add(current)
                    else:
                        if count in (1, 2):
                            new_bugs.add(current)
            new_layers[depth] = new_bugs
        self.layers = new_layers

    def neighbours(self, pos):
        for neighbour in neighbours(pos):
            if neighbour == self.CENTRE:
                # The centre, we need each of the 5 at the appropriate edge of the next level down
                diff = (neighbour[0] - pos[0], neighbour[1] - pos[1])
                for other in self.inner_transitions[diff]:
                    yield -1, other
            elif 0 <= neighbour[0] <= self.WIDTH and 0 <= neighbour[1] <= self.HEIGHT:
                yield 0, neighbour
            else:
                for other in self.outer_transitions[pos]:
                    yield 1, other

    def count_bugs(self):
        return sum(len(bugs) for bugs in self.layers.values())

    def __repr__(self):
        out = []
        for depth in range(self.bottom_layer, self.top_layer + 1):
            out.append(f"Depth {depth}:")

            for y in range(self.HEIGHT):
                line = []
                for x in range(self.WIDTH):
                    if (x, y) == self.CENTRE:
                        char = "?"
                    elif (x, y) in self.layers[depth]:
                        char = "#"
                    else:
                        char = "."
                    line.append(char)
                out.append("".join(line))
            out.append("")
        return "\n".join(out)


with open(sys.argv[1], "r") as file:
    lines = [line.strip() for line in file]

eris = Eris(lines)

step = 0
states = {eris.bugs: step}

while True:
    eris.step()
    if eris.bugs in states:
        print(eris.biodiversity())
        break

    step += 1
    states[eris.bugs] = step

eris = PlutonianEris(lines)

for i in range(10):
    eris.step()

print(eris)
print(eris.count_bugs())
