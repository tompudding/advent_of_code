import sys


class Vent:
    use_diagonal = True

    def __init__(self, start, end):
        self.start = tuple(start)
        self.end = tuple(end)
        self.diff = (end[0] - start[0], end[1] - start[1])
        # print(start, end, self.diff)
        # We want the diff vector to be as small as possible
        val = max((abs(v) for v in self.diff))
        self.diff = [v // val for v in self.diff]

    def points(self):
        if 0 not in self.diff and not self.use_diagonal:
            return
        pos = self.start
        while pos != self.end:
            yield pos
            pos = (pos[0] + self.diff[0], pos[1] + self.diff[1])
        yield self.end


class OrthoganalVent(Vent):
    use_diagonal = False


def parse_vent(line, cls):
    start, end = line.split(" -> ")
    return cls(*[[int(n) for n in point.split(",")] for point in (start, end)])


def get_points_at_least(cls, num):
    grid = {}
    count = 0

    with open(sys.argv[1], "r") as file:
        for line in file:
            vent = parse_vent(line.strip(), cls)
            for point in vent.points():
                try:
                    grid[point] += 1
                except KeyError:
                    grid[point] = 1

                if grid[point] == num:
                    count += 1

    return count


print(get_points_at_least(OrthoganalVent, 2))
print(get_points_at_least(Vent, 2))
