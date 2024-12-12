import sys
import collections
import enum


class Fence:
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3

    # These are turns where we stay in the same place
    turns = {
        TOP: ((0, 0), RIGHT, 1),
        RIGHT: ((0, 0), BOTTOM, 1),
        BOTTOM: ((0, 0), LEFT, 1),
        LEFT: ((0, 0), TOP, 1),
    }

    # These are interior turns
    # TOP -> RIGHT
    # _ _|A
    # A A A
    # Here we're
    other_turns = {
        TOP: ((1, -1), LEFT, 1),
        RIGHT: ((1, 1), TOP, 1),
        BOTTOM: ((-1, 1), RIGHT, 1),
        LEFT: ((-1, -1), BOTTOM, 1),
    }


class Directions:
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

    ALL = (UP, RIGHT, DOWN, LEFT)
    to_fence = {UP: Fence.TOP, DOWN: Fence.BOTTOM, LEFT: Fence.LEFT, RIGHT: Fence.RIGHT}


step_directions = {
    Fence.TOP: Directions.RIGHT,
    Fence.RIGHT: Directions.DOWN,
    Fence.BOTTOM: Directions.LEFT,
    Fence.LEFT: Directions.UP,
}


class Region:
    def __init__(self, plant, unused):
        # Build a region by filling from current, taking things from unused
        self.positions = set()
        self.plant = plant

        frontier = {next(iter(unused))}
        self.perimeter = 0
        self.fence_pieces = set()

        while frontier:
            pos = frontier.pop()
            self.positions.add(pos)

            # While we're doing this we can work out the perimeter
            perimeter = 0
            for direction in Directions.ALL:
                new_pos = (pos[0] + direction[0], pos[1] + direction[1])
                if new_pos not in unused:
                    self.fence_pieces.add((pos, Directions.to_fence[direction]))
                    perimeter += 1
                    continue
                if new_pos not in self.positions:
                    frontier.add(new_pos)

            self.perimeter += perimeter
        self.positions = frozenset(self.positions)

        # Now try to walk each fence
        unwalked = set(self.fence_pieces)
        walked = {}
        self.sides = 0
        while unwalked:
            path, sides = self.walk_fence(*next(iter(unwalked)))
            unwalked -= path
            self.sides += sides

    def walk_fence(self, pos, fence):
        start_pos = pos
        start_fence = fence
        sides = 0
        walked = set()
        current_fence = fence

        # Work out where we can go next
        next_positions = []

        while True:
            for movement, new_fence, extra_side in (
                (Fence.turns[fence]),
                (Fence.other_turns[fence]),
                (step_directions[fence], fence, 0),
            ):
                next_pos = (pos[0] + movement[0], pos[1] + movement[1])
                if (next_pos, new_fence) not in self.fence_pieces:
                    continue

                sides += extra_side

                if (next_pos, new_fence) in walked:
                    return walked, sides

                pos = next_pos
                fence = new_fence
                walked.add((pos, fence))
                break

            if (pos, fence) == (start_pos, start_fence):
                break

        return walked, sides

    def __repr__(self):
        return f"region[{self.plant}] : perim={self.perimeter} {self.positions}"

    def __hash__(self):
        return hash((self.plant, self.positions))

    def __eq__(self, other):
        return (self.plant, self.positions) == (other.plant, other.positions)


class Grid:
    def __init__(self, lines):
        self.grid = {}
        self.height = len(lines)
        self.width = len(lines[0])

        self.plants = collections.defaultdict(set)
        self.regions = collections.defaultdict(set)

        for y, row in enumerate(lines):
            for x, plant in enumerate(row):
                p = (x, y)
                self.plants[plant].add(p)

        # Now for each plant we'll flood-fill their regions
        for plant, positions in self.plants.items():
            unused = set(positions)

            while unused:
                region = Region(plant, unused)
                self.regions[plant].add(region)
                unused -= region.positions

    def get_cost(self):
        total = 0
        for plant, regions in self.regions.items():
            total += sum(region.perimeter * len(region.positions) for region in regions)

        return total

    def get_crazy_cost(self):
        total = 0
        for plant, regions in self.regions.items():
            total += sum(region.sides * len(region.positions) for region in regions)

        return total


with open(sys.argv[1], "r") as file:
    grid = Grid([line.strip() for line in file])

print(grid.get_cost())
print(grid.get_crazy_cost())
