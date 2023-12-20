import sys


class HeightMap:
    def __init__(self, lines):
        self.rows = []

        for line in lines:
            self.rows.append([int(c) for c in line.strip()])

        self.width = len(self.rows[0])
        self.height = len(self.rows)

    def neighbours(self, x, y):
        for diff in ((0, 1), (1, 0), (-1, 0), (0, -1)):
            point = x + diff[0], y + diff[1]
            if 0 <= point[0] < self.width and 0 <= point[1] < self.height:
                yield x + diff[0], y + diff[1]

    def low_points(self):
        for x in range(self.width):
            for y in range(self.height):
                val = self.rows[y][x]
                low_point = True
                for neighbour in self.neighbours(x, y):
                    if 0 <= neighbour[0] < self.width and 0 <= neighbour[1] < self.height:
                        neighbour_val = self.rows[neighbour[1]][neighbour[0]]

                        if neighbour_val <= val:
                            low_point = False
                            break
                if low_point:
                    print(x, y, val)
                    yield x, y, val

    def basin_size(self, x, y):
        basin = set()

        def add_neighbours(basin, x, y):
            for neighbour in self.neighbours(x, y):
                if neighbour in basin:
                    continue
                neighbour_val = self.rows[neighbour[1]][neighbour[0]]
                if neighbour_val == 9:
                    continue
                basin.add(neighbour)
                add_neighbours(basin, neighbour[0], neighbour[1])

        add_neighbours(basin, x, y)

        return len(basin)


with open(sys.argv[1], "r") as file:
    lines = file.readlines()

    height_map = HeightMap(lines)

part_one = 0
for x, y, low_point in height_map.low_points():
    part_one += low_point + 1

print(part_one)

sizes = []
for x, y, low_point in height_map.low_points():
    sizes.append(height_map.basin_size(x, y))

sizes.sort()
sizes = sizes[-3:]

part_two = 1
for size in sizes:
    part_two *= size

print(part_two)
