import sys
import functools


class Grid:
    def __init__(self, lines):
        self.width = len(lines[0])
        self.height = len(lines)
        self.splitters = set()

        for y in range(self.height):
            for x in range(self.width):
                if lines[y][x] == "^":
                    self.splitters.add((x, y))
        self.start_beam = {(lines[0].index("S"), 0)}

    def shoot_beam(self):
        beam_edge = set(self.start_beam)
        count = 0
        for row in range(self.height):
            splits = self.splitters & beam_edge
            count += len(splits)
            normal = beam_edge - splits

            beam_edge = (
                {(x, y + 1) for x, y in normal}
                | {(x - 1, y + 1) for x, y in splits}
                | {(x + 1, y + 1) for x, y in splits}
            )
        return count

    @functools.cache
    def count_timelines_cell(self, cell):
        if cell in self.splitters:
            return 0
        row = cell[1]
        if row == 0:
            return 1 if cell in self.start_beam else 0

        x = cell[0]
        total = self.count_timelines_cell((x, row - 1))
        if (x + 1, row) in self.splitters:
            total += self.count_timelines_cell((x + 1, row - 1))
        if (x - 1, row) in self.splitters:
            total += self.count_timelines_cell((x - 1, row - 1))
        return total

    def count_timelines(self):
        return sum(self.count_timelines_cell((x, self.height - 1)) for x in range(self.width))


with open(sys.argv[1]) as file:
    grid = Grid([line.strip() for line in file])

print(grid.shoot_beam())
print(grid.count_timelines())
